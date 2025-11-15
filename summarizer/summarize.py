"""summarizer.summarize

Simple, reusable book summarization helpers for TARS.
"""

from __future__ import annotations

import json
import os
import re
from typing import List, Dict

import openai
from PyPDF2 import PdfReader

DEFAULT_MODEL = os.getenv("OPENAI_MODEL", "gpt-4")

def _require_api_key() -> None:
	"""Ensure OPENAI_API_KEY is set in environment."""
	if not os.getenv("OPENAI_API_KEY"):
		raise RuntimeError(
			"OPENAI_API_KEY environment variable is required to call the OpenAI API."
		)
	openai.api_key = os.getenv("OPENAI_API_KEY")

def extract_text_from_pdf(path: str) -> str:
	"""Extract text from a PDF file using PyPDF2.

	Returns concatenated page text.
	"""
	reader = PdfReader(path)
	texts: List[str] = []
	for page in reader.pages:
		try:
			texts.append(page.extract_text() or "")
		except Exception:
			# If any page fails, continue with what we have
			continue
	return "\n\n".join(texts)

def read_text_file(path: str) -> str:
	"""Read a plain text file and return its contents."""
	with open(path, "r", encoding="utf-8") as f:
		return f.read()

def clean_text(text: str) -> str:
	"""Do light normalization of extracted text.

	- Normalize whitespace
	- Remove repeated page headers/footers heuristically
	"""
	if not text:
		return ""
	# Replace Windows line endings and normalize whitespace
	t = text.replace("\r\n", "\n").replace("\r", "\n")
	# Remove sequences of 3+ newlines
	t = re.sub(r"\n{3,}", "\n\n", t)
	# Collapse multiple spaces
	t = re.sub(r"[ \t]{2,}", " ", t)
	# Trim
	return t.strip()

def chunk_text(text: str, max_chars: int = 6000) -> List[str]:
	"""Split text into chunks of approximately `max_chars` characters.

	This function splits on paragraph boundaries when possible.
	"""
	if not text:
		return []
	paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
	chunks: List[str] = []
	current = []
	current_len = 0

	for p in paragraphs:
		if current_len + len(p) + 2 <= max_chars:
			current.append(p)
			current_len += len(p) + 2
		else:
			if current:
				chunks.append("\n\n".join(current))
			# If single paragraph is larger than max_chars, split it
			if len(p) > max_chars:
				for i in range(0, len(p), max_chars):
					chunks.append(p[i : i + max_chars])
				current = []
				current_len = 0
			else:
				current = [p]
				current_len = len(p) + 2

	if current:
		chunks.append("\n\n".join(current))

	return chunks

def _build_chunk_prompt(text_chunk: str) -> str:
	"""Return a user prompt asking the model to summarize one chunk.

	We instruct the model to return JSON only so parsing is straightforward.
	"""
	prompt = (
		"You are a helpful assistant that extracts structured summaries from book content.\n\n"
		"Please produce a JSON object with the following fields: `tldr` (a 3-sentence summary),"
		" `key_points` (an array of 5 concise bullet points), and `questions` (an array of 3 important questions the content answers).\n\n"
		"The JSON must be the only content in your response. Do not include commentary or explanation.\n\n"
		"Here is the content to summarize:\n\n" + text_chunk
	)
	return prompt

def summarize_chunk(text_chunk: str, model: str = DEFAULT_MODEL) -> Dict:
	"""Call OpenAI to summarize a single chunk and parse JSON output.

	Returns a dict with keys: tldr, key_points, questions.
	"""
	_require_api_key()
	prompt = _build_chunk_prompt(text_chunk)

	resp = openai.ChatCompletion.create(
		model=model,
		messages=[
			{"role": "system", "content": "You are a concise summarization assistant."},
			{"role": "user", "content": prompt},
		],
		temperature=0.15,
		max_tokens=700,
	)

	text = resp.choices[0].message["content"].strip()

	try:
		parsed = json.loads(text)
		# Validate keys exist
		return {
			"tldr": parsed.get("tldr", "").strip(),
			"key_points": parsed.get("key_points", [])[:5],
			"questions": parsed.get("questions", [])[:3],
		}
	except Exception:
		# Fallback: try to extract lines heuristically
		lines = [l.strip() for l in text.splitlines() if l.strip()]
		tldr = ""
		key_points: List[str] = []
		questions: List[str] = []
		for line in lines:
			if not tldr and len(line.split()) >= 5:
				tldr = line
			elif line.startswith("-") or line.startswith("*"):
				key_points.append(line.lstrip("-* "))
			elif line.endswith("?"):
				questions.append(line)

		return {"tldr": tldr, "key_points": key_points[:5], "questions": questions[:3]}

def synthesize_summaries(partial_summaries: List[Dict], model: str = DEFAULT_MODEL) -> Dict:
	"""Take per-chunk summaries and ask the model to synthesize a final JSON summary.

	`partial_summaries` is a list of dicts produced by `summarize_chunk`.
	"""
	_require_api_key()
	# Build an aggregation prompt containing the JSON summaries
	summaries_json = json.dumps(partial_summaries, ensure_ascii=False, indent=2)
	prompt = (
		"You are an expert assistant that combines multiple partial summaries into a single, coherent structured summary.\n\n"
		"Each item in the provided JSON array is an object with `tldr`, `key_points`, and `questions`.\n\n"
		"Produce a single JSON object with `tldr` (3 sentences), `key_points` (5 concise bullets), and `questions` (3 questions)."
		" Use the input as source material; synthesize and deduplicate ideas. Return JSON only.\n\nInput:\n"
		+ summaries_json
	)

	resp = openai.ChatCompletion.create(
		model=model,
		messages=[
			{"role": "system", "content": "You are a concise summarization assistant."},
			{"role": "user", "content": prompt},
		],
		temperature=0.12,
		max_tokens=700,
	)

	text = resp.choices[0].message["content"].strip()
	try:
		parsed = json.loads(text)
		return {
			"tldr": parsed.get("tldr", "").strip(),
			"key_points": parsed.get("key_points", [])[:5],
			"questions": parsed.get("questions", [])[:3],
		}
	except Exception:
		# If parsing fails, return a naive merge
		tldr = " ".join([s.get("tldr", "") for s in partial_summaries])
		key_points = []
		questions = []
		for s in partial_summaries:
			key_points.extend(s.get("key_points", []))
			questions.extend(s.get("questions", []))
		# Deduplicate while preserving order
		def dedupe(seq):
			seen = set()
			out = []
			for item in seq:
				if item and item not in seen:
					seen.add(item)
					out.append(item)
			return out

		return {
			"tldr": (tldr.strip()[:1000] if tldr else ""),
			"key_points": dedupe(key_points)[:5],
			"questions": dedupe(questions)[:3],
		}

def summarize_text(input_text: str) -> Dict:
	"""Top-level function: accept raw text, chunk it, summarize each chunk, and synthesize.

	Returns the final structured summary.
	"""
	text = clean_text(input_text)
	if not text:
		return {"tldr": "", "key_points": [], "questions": []}

	chunks = chunk_text(text)
	if not chunks:
		return {"tldr": "", "key_points": [], "questions": []}

	partials = []
	for i, c in enumerate(chunks):
		# For long documents this will make multiple API calls (one per chunk)
		print(f"Summarizing chunk {i+1}/{len(chunks)} (approx {len(c)} chars)")
		s = summarize_chunk(c)
		partials.append(s)

	# Synthesize
	final = synthesize_summaries(partials)
	return final

def summarize_file(path: str) -> Dict:
	"""Detect the file type and summarize its contents."""
	if path.lower().endswith(".pdf"):
		raw = extract_text_from_pdf(path)
	else:
		raw = read_text_file(path)
	return summarize_text(raw)

if __name__ == "__main__":
	# Quick local test runner: will summarize data/sample_text.txt if present
	sample_txt = os.path.join(os.path.dirname(__file__), "..", "data", "sample_text.txt")
	sample_txt = os.path.normpath(sample_txt)
	if not os.path.exists(sample_txt):
		print("No sample file found at:", sample_txt)
		print("To test, set OPENAI_API_KEY and create data/sample_text.txt or call summarize_text(text)")
	else:
		try:
			print("Running local summarization test on:", sample_txt)
			summary = summarize_file(sample_txt)
			print(json.dumps(summary, ensure_ascii=False, indent=2))
		except Exception as e:
			print("Error during summarization:", e)


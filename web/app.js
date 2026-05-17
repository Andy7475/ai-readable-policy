'use strict';

const GEMINI_URL = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent';
const INDEX_URL = './search-index.json';
const TOP_N_CHUNKS = 8;
const LS_KEY_APIKEY = 'policy-demo-api-key';

const STOPWORDS = new Set([
  'a','an','the','and','or','but','in','on','at','to','for','of','with','by',
  'from','as','is','are','was','were','be','been','being','have','has','had',
  'do','does','did','will','would','could','should','may','might','must',
  'shall','can','not','this','that','these','those','it','its','their','they',
  'all','any','each','both','few','more','most','other','into','through','than',
  'so','if','no','up','out','about','such',
]);

const SYSTEM_INSTRUCTION = `You are a policy compliance assistant. You help users find relevant policy information.

Respond with valid JSON only — no markdown fences, no prose outside the JSON.

Rules:
1. Answer using ONLY the provided policy sections. Do not use outside knowledge.
2. Keep your answer to 1-3 sentences. It should directly address the question.
3. Cite every section that supports your answer using its exact section_id and policy_file from the context.
4. Do not paraphrase or quote policy text — the UI will display the verbatim text.
5. If no provided section answers the question, set answer to "The provided policy sections do not appear to cover this question." and return an empty citations array.

Response schema (JSON only):
{
  "answer": "<1-3 sentence direct answer>",
  "citations": [
    {
      "section_id": "<exact section_id from context>",
      "policy_file": "<exact policy_file from context>",
      "relevance": "<one sentence: why this section is relevant>"
    }
  ]
}`;

// ── State ────────────────────────────────────────────────────────────────────

const state = {
  index: null,
  chunkMap: {},
};

// ── Utilities ────────────────────────────────────────────────────────────────

function escapeHtml(str) {
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

function tokenise(text) {
  return text.toLowerCase().replace(/[^a-z\s]/g, '').split(/\s+/).filter(
    t => t.length >= 3 && !STOPWORDS.has(t)
  );
}

function findRelevantChunks(query) {
  const queryTerms = new Set(tokenise(query));
  if (queryTerms.size === 0) return [];
  return state.index.chunks
    .map(chunk => ({ chunk, score: chunk.terms.filter(t => queryTerms.has(t)).length }))
    .filter(x => x.score > 0)
    .sort((a, b) => b.score - a.score)
    .slice(0, TOP_N_CHUNKS)
    .map(x => x.chunk);
}

function buildContextText(chunks) {
  return chunks.map(c =>
    `--- Section: ${c.section_title} (section_id: "${c.section_id}", policy_file: "${c.policy_file}")\n${c.text}`
  ).join('\n\n');
}

// ── DOM helpers ──────────────────────────────────────────────────────────────

function showError(msg) {
  const el = document.getElementById('error-banner');
  el.textContent = msg;
  el.hidden = false;
}

function clearError() {
  const el = document.getElementById('error-banner');
  el.hidden = true;
  el.textContent = '';
}

function setLoading(on) {
  document.getElementById('loading-indicator').hidden = !on;
  document.getElementById('search-btn').disabled = on;
}

function renderAnswer(parsed, chunks) {
  const answerSection = document.getElementById('answer-section');
  const answerText = document.getElementById('answer-text');
  const citationsContainer = document.getElementById('citations-container');

  answerText.textContent = parsed.answer;
  citationsContainer.innerHTML = '';

  const validCitations = (parsed.citations || []).filter(
    cit => state.chunkMap[cit.section_id]
  );

  if (validCitations.length === 0) {
    answerSection.hidden = false;
    return;
  }

  const heading = document.createElement('h3');
  heading.textContent = 'Policy References';
  citationsContainer.appendChild(heading);

  for (const cit of validCitations) {
    const chunk = state.chunkMap[cit.section_id];
    const url = new URL(chunk.policy_file + '#' + chunk.section_id, window.location.href).href;

    const card = document.createElement('div');
    card.className = 'citation-card';

    const cardHeader = document.createElement('div');
    cardHeader.className = 'citation-header';

    const policyName = document.createElement('span');
    policyName.className = 'policy-name';
    policyName.textContent = chunk.policy_title;

    const sectionLink = document.createElement('a');
    sectionLink.className = 'section-link';
    sectionLink.href = url;
    sectionLink.target = '_blank';
    sectionLink.rel = 'noopener noreferrer';
    sectionLink.textContent = chunk.section_title + ' ↗';

    const relevanceNote = document.createElement('p');
    relevanceNote.className = 'relevance-note';
    relevanceNote.textContent = cit.relevance;

    const verbatim = document.createElement('blockquote');
    verbatim.className = 'verbatim-text';
    verbatim.textContent = chunk.text;

    cardHeader.appendChild(policyName);
    cardHeader.appendChild(sectionLink);
    card.appendChild(cardHeader);
    card.appendChild(relevanceNote);
    card.appendChild(verbatim);
    citationsContainer.appendChild(card);
  }

  answerSection.hidden = false;
}

// ── Gemini API call ──────────────────────────────────────────────────────────

async function askGemini(query, chunks) {
  const apiKey = document.getElementById('api-key-input').value.trim();
  if (!apiKey) {
    showError('Please enter your Google AI Studio API key.');
    return null;
  }

  const contextText = buildContextText(chunks);
  const userMessage = chunks.length > 0
    ? `Question: ${query}\n\nRelevant policy sections:\n${contextText}`
    : `Question: ${query}\n\n(No matching sections found in the policy index.)`;

  const body = {
    system_instruction: { parts: [{ text: SYSTEM_INSTRUCTION }] },
    contents: [{ role: 'user', parts: [{ text: userMessage }] }],
    generationConfig: { responseMimeType: 'application/json' },
  };

  const response = await fetch(`${GEMINI_URL}?key=${encodeURIComponent(apiKey)}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });

  if (!response.ok) {
    const errText = await response.text().catch(() => response.statusText);
    throw new Error(`Gemini API error ${response.status}: ${errText}`);
  }

  const data = await response.json();
  const rawText = data?.candidates?.[0]?.content?.parts?.[0]?.text;
  if (!rawText) throw new Error('Unexpected response shape from Gemini.');

  return JSON.parse(rawText);
}

// ── Event handlers ───────────────────────────────────────────────────────────

async function handleSearch() {
  clearError();
  document.getElementById('answer-section').hidden = true;

  const query = document.getElementById('query-input').value.trim();
  if (!query) { showError('Please enter a question.'); return; }

  if (!state.index) { showError('Search index not loaded yet. Please wait.'); return; }

  setLoading(true);
  try {
    const chunks = findRelevantChunks(query);
    const parsed = await askGemini(query, chunks);
    if (parsed) renderAnswer(parsed, chunks);
  } catch (err) {
    showError(err.message || 'An unexpected error occurred.');
  } finally {
    setLoading(false);
  }
}

function handleSaveKey() {
  const key = document.getElementById('api-key-input').value.trim();
  if (key) {
    localStorage.setItem(LS_KEY_APIKEY, key);
    document.getElementById('key-status').textContent = 'Saved.';
    setTimeout(() => { document.getElementById('key-status').textContent = ''; }, 2000);
  }
}

// ── Initialisation ───────────────────────────────────────────────────────────

async function init() {
  const savedKey = localStorage.getItem(LS_KEY_APIKEY);
  if (savedKey) document.getElementById('api-key-input').value = savedKey;

  try {
    const resp = await fetch(INDEX_URL);
    if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
    state.index = await resp.json();
    state.chunkMap = Object.fromEntries(state.index.chunks.map(c => [c.section_id, c]));
    const info = document.getElementById('index-info');
    if (info) {
      info.textContent =
        `${state.index.chunks.length} sections indexed across ${state.index.policies.length} policies.`;
    }
  } catch (err) {
    showError(`Could not load search index: ${err.message}`);
  }

  document.getElementById('search-btn').addEventListener('click', handleSearch);
  document.getElementById('save-key-btn').addEventListener('click', handleSaveKey);
  document.getElementById('query-input').addEventListener('keydown', e => {
    if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) handleSearch();
  });
}

document.addEventListener('DOMContentLoaded', init);

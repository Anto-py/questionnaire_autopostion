/**
 * Netlify Function — proxy sécurisé vers les APIs d'IA
 * La clé API reste sur le serveur (variable d'environnement Netlify)
 * et n'est jamais exposée côté client.
 *
 * Variables d'environnement à configurer dans le dashboard Netlify :
 *   AI_PROVIDER   — 'anthropic' (défaut) | 'openai'
 *   AI_API_KEY    — votre clé API
 *   AI_MODEL      — optionnel, remplace le modèle par défaut
 */

const DEFAULTS = {
  anthropic: { model: 'claude-sonnet-4-6', url: 'https://api.anthropic.com/v1/messages' },
  openai:    { model: 'gpt-4o',            url: 'https://api.openai.com/v1/chat/completions' }
};

exports.handler = async (event) => {
  const cors = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Allow-Methods': 'POST, OPTIONS'
  };

  if (event.httpMethod === 'OPTIONS') {
    return { statusCode: 204, headers: cors, body: '' };
  }

  if (event.httpMethod !== 'POST') {
    return { statusCode: 405, headers: cors, body: 'Method Not Allowed' };
  }

  const apiKey   = process.env.AI_API_KEY;
  const provider = (process.env.AI_PROVIDER || 'anthropic').toLowerCase();

  if (!apiKey) {
    return {
      statusCode: 500,
      headers: { ...cors, 'Content-Type': 'application/json' },
      body: JSON.stringify({ error: { message: 'AI_API_KEY non configurée dans les variables Netlify.' } })
    };
  }

  let body;
  try {
    body = JSON.parse(event.body);
  } catch {
    return { statusCode: 400, headers: cors, body: 'JSON invalide' };
  }

  const { systemPrompt, userContent } = body;
  const model = process.env.AI_MODEL || DEFAULTS[provider]?.model || 'claude-sonnet-4-6';
  const apiUrl = DEFAULTS[provider]?.url || DEFAULTS.anthropic.url;

  let reqBody, reqHeaders;

  if (provider === 'anthropic') {
    reqBody = JSON.stringify({
      model,
      max_tokens: 1200,
      temperature: 0.4,
      system: systemPrompt,
      messages: [{ role: 'user', content: userContent }]
    });
    reqHeaders = {
      'Content-Type': 'application/json',
      'x-api-key': apiKey,
      'anthropic-version': '2023-06-01'
    };
  } else {
    reqBody = JSON.stringify({
      model,
      max_tokens: 1200,
      temperature: 0.4,
      messages: [
        { role: 'system', content: systemPrompt },
        { role: 'user', content: userContent }
      ]
    });
    reqHeaders = {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer ' + apiKey
    };
  }

  try {
    const resp = await fetch(apiUrl, { method: 'POST', headers: reqHeaders, body: reqBody });
    const data = await resp.json();

    if (!resp.ok) {
      return {
        statusCode: resp.status,
        headers: { ...cors, 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      };
    }

    const text = provider === 'anthropic'
      ? data.content[0].text
      : data.choices[0].message.content;

    return {
      statusCode: 200,
      headers: { ...cors, 'Content-Type': 'application/json' },
      body: JSON.stringify({ text })
    };

  } catch (err) {
    return {
      statusCode: 502,
      headers: { ...cors, 'Content-Type': 'application/json' },
      body: JSON.stringify({ error: { message: err.message } })
    };
  }
};

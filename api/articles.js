const https = require('https');

module.exports = async (req, res) => {
  const supabaseUrl = process.env.SUPABASE_URL || 'https://keajnbcsqgyfgyikvbca.supabase.co';
  const supabaseKey = process.env.SUPABASE_ANON_KEY || process.env.SUPABASE_SERVICE_KEY || 'sb_publishable_tUM51WsQtzlmiiLABjCnBw_N3HeE0ay';

  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    res.status(200).end();
    return;
  }

  try {
    const url = `${supabaseUrl}/rest/v1/articles?select=*&order=published_at.desc`;
    
    const options = {
      headers: {
        'apikey': supabaseKey,
        'Authorization': `Bearer ${supabaseKey}`,
        'Content-Type': 'application/json'
      }
    };

    const articles = await new Promise((resolve, reject) => {
      https.get(url, options, (response) => {
        let data = '';
        
        response.on('data', (chunk) => {
          data += chunk;
        });
        
        response.on('end', () => {
          try {
            resolve(JSON.parse(data));
          } catch (e) {
            reject(new Error('Failed to parse response'));
          }
        });
      }).on('error', reject);
    });

    const processedArticles = articles.map(article => ({
      id: article.id,
      title: article.title,
      source: article.source,
      url: article.url,
      summary: article.subtitle || article.summary || '',
      published_at: article.published_at,
      category: article.category || 'AI News',
      author: article.author || 'Unknown',
      image_url: article.image_url || '',
      is_saved: false
    }));

    res.setHeader('Cache-Control', 's-maxage=60, stale-while-revalidate');
    res.status(200).json({ 
      success: true, 
      articles: processedArticles,
      count: processedArticles.length 
    });

  } catch (error) {
    console.error('Error fetching articles:', error);
    res.status(500).json({ 
      success: false, 
      error: error.message 
    });
  }
};

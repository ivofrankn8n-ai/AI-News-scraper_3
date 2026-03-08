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
    const articlesUrl = `${supabaseUrl}/rest/v1/articles?select=*&order=published_at.desc`;
    const metadataUrl = `${supabaseUrl}/rest/v1/scraper_metadata?select=last_scraped_at&source=eq.all&limit=1`;
    
    const options = {
      headers: {
        'apikey': supabaseKey,
        'Authorization': `Bearer ${supabaseKey}`,
        'Content-Type': 'application/json'
      }
    };

    const [articlesResponse, metadataResponse] = await Promise.all([
      new Promise((resolve, reject) => {
        https.get(articlesUrl, options, (response) => {
          let data = '';
          response.on('data', (chunk) => data += chunk);
          response.on('end', () => {
            try { resolve(JSON.parse(data)); } catch (e) { reject(e); }
          });
        }).on('error', reject);
      }),
      new Promise((resolve, reject) => {
        https.get(metadataUrl, options, (response) => {
          let data = '';
          response.on('data', (chunk) => data += chunk);
          response.on('end', () => {
            try { resolve(JSON.parse(data)); } catch (e) { reject(e); }
          });
        }).on('error', reject);
      })
    ]);

    const articles = articlesResponse;
    const metadata = metadataResponse[0] || null;

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
      count: processedArticles.length,
      last_scraped_at: metadata?.last_scraped_at || null
    });

  } catch (error) {
    console.error('Error fetching articles:', error);
    res.status(500).json({ 
      success: false, 
      error: error.message 
    });
  }
};

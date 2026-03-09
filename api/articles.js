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
    // Get time filter from query parameter (default: 'all')
    // Use URL parsing for reliable parameter extraction
    const url = new URL(req.url, `http://${req.headers.host}`);
    const searchParams = new URLSearchParams(url.search);
    const timeFilter = searchParams.get('timeFilter') || 'all';
    
    // Build date filter based on time range
    let dateFilter = '';
    const now = new Date();
    
    switch (timeFilter) {
      case '6h':
        const sixHoursAgo = new Date(now.getTime() - 6 * 60 * 60 * 1000).toISOString();
        dateFilter = `published_at=gte.${sixHoursAgo}`;
        break;
      case '1day':
        const oneDayAgo = new Date(now.getTime() - 24 * 60 * 60 * 1000).toISOString();
        dateFilter = `published_at=gte.${oneDayAgo}`;
        break;
      case '2days':
        const twoDaysAgo = new Date(now.getTime() - 2 * 24 * 60 * 60 * 1000).toISOString();
        dateFilter = `published_at=gte.${twoDaysAgo}`;
        break;
      case '3days':
        const threeDaysAgo = new Date(now.getTime() - 3 * 24 * 60 * 60 * 1000).toISOString();
        dateFilter = `published_at=gte.${threeDaysAgo}`;
        break;
      case '1week':
        const oneWeekAgo = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000).toISOString();
        dateFilter = `published_at=gte.${oneWeekAgo}`;
        break;
      case '2weeks':
        const twoWeeksAgo = new Date(now.getTime() - 14 * 24 * 60 * 60 * 1000).toISOString();
        dateFilter = `published_at=gte.${twoWeeksAgo}`;
        break;
      case '3weeks':
        const threeWeeksAgo = new Date(now.getTime() - 21 * 24 * 60 * 60 * 1000).toISOString();
        dateFilter = `published_at=gte.${threeWeeksAgo}`;
        break;
      case '1month':
        const oneMonthAgo = new Date(now.getTime() - 30 * 24 * 60 * 60 * 1000).toISOString();
        dateFilter = `published_at=gte.${oneMonthAgo}`;
        break;
      case '2months':
        const twoMonthsAgo = new Date(now.getTime() - 60 * 24 * 60 * 60 * 1000).toISOString();
        dateFilter = `published_at=gte.${twoMonthsAgo}`;
        break;
      case '3months':
        const threeMonthsAgo = new Date(now.getTime() - 90 * 24 * 60 * 60 * 1000).toISOString();
        dateFilter = `published_at=gte.${threeMonthsAgo}`;
        break;
      case '6months':
        const sixMonthsAgo = new Date(now.getTime() - 180 * 24 * 60 * 60 * 1000).toISOString();
        dateFilter = `published_at=gte.${sixMonthsAgo}`;
        break;
      case '1year':
        const oneYearAgo = new Date(now.getTime() - 365 * 24 * 60 * 60 * 1000).toISOString();
        dateFilter = `published_at=gte.${oneYearAgo}`;
        break;
      case 'all':
      default:
        dateFilter = ''; // No filter
    }
    
    // Build articles URL with optional date filter
    let articlesUrl = `${supabaseUrl}/rest/v1/articles?select=*&order=published_at.desc`;
    if (dateFilter) {
      articlesUrl += `&${dateFilter}`;
    }
    
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

    res.status(200).json({ 
      success: true, 
      articles: processedArticles,
      count: processedArticles.length,
      last_scraped_at: metadata?.last_scraped_at || null,
      time_filter: timeFilter
    });

  } catch (error) {
    console.error('Error fetching articles:', error);
    res.status(500).json({ 
      success: false, 
      error: error.message 
    });
  }
};

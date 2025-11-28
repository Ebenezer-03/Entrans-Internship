import pandas as pd
import random
from datetime import datetime, timedelta

# News templates by category
NEWS_TEMPLATES = {
    'Technology': [
        '{company} announces breakthrough in {tech_topic}, expected to revolutionize the industry',
        'New {device} from {company} features {feature}, launching {timeframe}',
        '{tech_topic} adoption grows {percent}% as companies embrace digital transformation',
        'Cybersecurity experts warn about new {threat} targeting {target}',
        'AI-powered {application} achieves {achievement}, surpassing human performance',
        '{company} invests ${amount} million in {tech_topic} research',
        'Open-source {project} reaches {milestone} downloads, community celebrates',
        'Quantum computing breakthrough: {achievement} demonstrated by {company}',
        '{tech_topic} market projected to reach ${amount} billion by {year}',
        'Privacy concerns raised over {company}\'s new {feature} feature'
    ],
    'Business': [
        '{company} reports {percent}% {direction} in Q{quarter} earnings, beating analyst expectations',
        'Stock market {direction} as {indicator} shows {trend}',
        'Merger announced: {company} to acquire {company2} for ${amount} billion',
        '{industry} sector faces challenges amid {economic_factor}',
        'Startup {company} raises ${amount} million in Series {series} funding',
        'CEO of {company} steps down amid {reason}',
        'New trade agreement signed between {country} and {country2}',
        '{company} announces {percent}% workforce expansion in {region}',
        'Economic forecast predicts {trend} for {timeframe}',
        'Inflation {direction} to {percent}% as {factor} stabilizes'
    ],
    'Sports': [
        '{team} defeats {team2} {score} in thrilling {sport} match',
        '{athlete} breaks {record} record at {event}',
        '{team} signs {athlete} to ${amount} million contract',
        'Olympic preparations underway for {city} {year} games',
        '{team} clinches {championship} title after {achievement}',
        'Injury sidelines {athlete} for {timeframe}, team adjusts strategy',
        '{sport} finals: {team} vs {team2} set for {date}',
        'Controversy erupts over {issue} in {sport} championship',
        '{athlete} announces retirement after {years}-year career',
        'World Cup qualifier: {country} advances after {score} victory'
    ],
    'Politics': [
        '{country} announces new {policy} policy, effective {timeframe}',
        'Election results: {candidate} wins {position} with {percent}% of votes',
        'Diplomatic tensions rise between {country} and {country2} over {issue}',
        'New legislation proposed to address {issue}',
        '{leader} meets with {leader2} to discuss {topic}',
        'Parliament passes {bill} bill after months of debate',
        'Protests erupt in {city} demanding {change}',
        'Coalition government formed in {country} after {event}',
        '{position} nominee faces scrutiny over {issue}',
        'International summit focuses on {global_issue}'
    ],
    'Science': [
        'Scientists discover new {discovery} in {location}',
        'Breakthrough in {field} research could lead to {application}',
        'NASA mission to {planet} reveals {finding}',
        'New species of {organism} found in {habitat}',
        'Climate study shows {trend} in {region}',
        'Medical researchers develop promising {treatment} for {disease}',
        'Archaeological dig uncovers {artifact} dating back {timeframe}',
        'Space telescope captures unprecedented images of {celestial_object}',
        'Geneticists make progress in understanding {genetic_topic}',
        'Environmental study highlights {concern} in {ecosystem}'
    ],
    'Health': [
        'New study links {factor} to reduced risk of {disease}',
        'Health officials recommend {action} to prevent {illness}',
        'Breakthrough treatment for {disease} shows {percent}% success rate',
        'Mental health awareness campaign launches focusing on {topic}',
        'Vaccine development for {disease} enters phase {phase} trials',
        'Nutrition research suggests {finding} about {food}',
        'Fitness trend: {exercise} gains popularity for {benefit}',
        'Hospital implements new {technology} to improve patient care',
        'Public health warning issued about {threat}',
        'Wellness program reduces {condition} cases by {percent}%'
    ],
    'Entertainment': [
        '{celebrity} wins {award} for {work}',
        'New {genre} film "{title}" breaks box office records',
        '{artist} announces world tour with {number} shows',
        'Streaming service {platform} releases {show}, critics praise {aspect}',
        'Music festival {event} announces {artist} as headliner',
        '{celebrity} launches {product} brand',
        'Award show controversy: {issue} sparks debate',
        'Behind the scenes: making of "{title}" documentary released',
        '{artist} collaborates with {artist2} on new {project}',
        'Gaming: {game} surpasses {number} million players globally'
    ]
}

# Data pools
COMPANIES = ['Apple', 'Google', 'Microsoft', 'Tesla', 'Amazon', 'Meta', 'Samsung', 'Intel', 'NVIDIA', 'IBM', 'Oracle', 'Salesforce', 'Adobe', 'Netflix', 'Toyota', 'BMW', 'Ford', 'Pfizer', 'Johnson & Johnson', 'ExxonMobil']
TECH_TOPICS = ['AI', 'blockchain', 'cloud computing', 'quantum computing', '5G', 'IoT', 'machine learning', 'autonomous vehicles', 'robotics', 'cybersecurity']
DEVICES = ['smartphone', 'laptop', 'tablet', 'smartwatch', 'VR headset', 'smart home device']
COUNTRIES = ['USA', 'China', 'India', 'Germany', 'France', 'UK', 'Japan', 'Brazil', 'Canada', 'Australia']
TEAMS = ['Lakers', 'Warriors', 'Patriots', 'Yankees', 'Real Madrid', 'Barcelona', 'Manchester United', 'Bayern Munich']
ATHLETES = ['LeBron James', 'Serena Williams', 'Lionel Messi', 'Cristiano Ronaldo', 'Novak Djokovic', 'Simone Biles']
DISEASES = ['cancer', 'diabetes', 'heart disease', 'Alzheimer\'s', 'Parkinson\'s', 'arthritis']

def generate_news_article(category):
    """Generate a single realistic news article"""
    template = random.choice(NEWS_TEMPLATES[category])
    
    # Fill in placeholders
    article = template.format(
        company=random.choice(COMPANIES),
        company2=random.choice(COMPANIES),
        tech_topic=random.choice(TECH_TOPICS),
        device=random.choice(DEVICES),
        feature=random.choice(['AI integration', 'improved battery life', 'enhanced security', 'faster processor']),
        timeframe=random.choice(['next month', 'Q3', 'this year', 'in 2026']),
        percent=random.randint(5, 95),
        threat=random.choice(['malware', 'ransomware', 'phishing campaign', 'zero-day exploit']),
        target=random.choice(['enterprises', 'consumers', 'government agencies', 'healthcare systems']),
        application=random.choice(['chatbot', 'diagnostic tool', 'recommendation system', 'translation service']),
        achievement=random.choice(['95% accuracy', 'record-breaking speed', 'human-level performance']),
        amount=random.randint(10, 999),
        project=random.choice(['framework', 'library', 'platform', 'tool']),
        milestone=random.choice(['1 million', '10 million', '100 million']),
        year=random.randint(2025, 2030),
        direction=random.choice(['rise', 'increase', 'surge', 'decline', 'drop']),
        quarter=random.randint(1, 4),
        indicator=random.choice(['GDP', 'unemployment rate', 'inflation', 'consumer confidence']),
        trend=random.choice(['growth', 'stability', 'volatility', 'improvement']),
        industry=random.choice(['tech', 'automotive', 'retail', 'energy', 'healthcare']),
        economic_factor=random.choice(['inflation', 'supply chain issues', 'labor shortage', 'regulatory changes']),
        series=random.choice(['A', 'B', 'C', 'D']),
        reason=random.choice(['restructuring', 'strategic differences', 'retirement', 'controversy']),
        country=random.choice(COUNTRIES),
        country2=random.choice(COUNTRIES),
        region=random.choice(['Asia', 'Europe', 'North America', 'Latin America']),
        team=random.choice(TEAMS),
        team2=random.choice(TEAMS),
        athlete=random.choice(ATHLETES),
        score=f"{random.randint(0, 5)}-{random.randint(0, 5)}",
        sport=random.choice(['football', 'basketball', 'tennis', 'soccer']),
        record=random.choice(['world', 'Olympic', 'season', 'career']),
        event=random.choice(['Olympics', 'World Championships', 'Grand Slam']),
        championship=random.choice(['league', 'division', 'regional', 'national']),
        years=random.randint(10, 25),
        date=random.choice(['Sunday', 'next week', 'this weekend']),
        issue=random.choice(['doping allegations', 'rule changes', 'scheduling conflicts']),
        policy=random.choice(['environmental', 'economic', 'education', 'healthcare']),
        candidate=random.choice(['John Smith', 'Jane Doe', 'Michael Brown', 'Sarah Johnson']),
        position=random.choice(['President', 'Governor', 'Senator', 'Mayor']),
        leader=random.choice(['President', 'Prime Minister', 'Chancellor']),
        leader2=random.choice(['President', 'Prime Minister', 'King']),
        topic=random.choice(['trade', 'security', 'climate change', 'immigration']),
        bill=random.choice(['healthcare reform', 'infrastructure', 'education funding', 'tax reform']),
        city=random.choice(['London', 'Paris', 'New York', 'Tokyo', 'Delhi']),
        change=random.choice(['policy reform', 'government transparency', 'workers\' rights']),
        global_issue=random.choice(['climate change', 'poverty', 'human rights', 'pandemic response']),
        discovery=random.choice(['planet', 'molecule', 'fossil', 'phenomenon']),
        location=random.choice(['Amazon', 'Antarctica', 'deep ocean', 'space']),
        field=random.choice(['cancer', 'renewable energy', 'neuroscience', 'materials science']),
        planet=random.choice(['Mars', 'Jupiter', 'Saturn', 'Venus']),
        finding=random.choice(['water deposits', 'atmospheric anomalies', 'geological formations']),
        organism=random.choice(['fish', 'insect', 'plant', 'mammal']),
        habitat=random.choice(['rainforest', 'coral reef', 'mountain range', 'cave system']),
        treatment=random.choice(['therapy', 'medication', 'procedure', 'vaccine']),
        disease=random.choice(DISEASES),
        artifact=random.choice(['temple', 'manuscript', 'tool', 'pottery']),
        celestial_object=random.choice(['galaxy', 'nebula', 'exoplanet', 'black hole']),
        genetic_topic=random.choice(['longevity', 'disease resistance', 'intelligence', 'aging']),
        concern=random.choice(['biodiversity loss', 'pollution', 'habitat destruction']),
        ecosystem=random.choice(['rainforest', 'ocean', 'grassland', 'wetland']),
        factor=random.choice(['exercise', 'diet', 'sleep', 'stress management']),
        illness=random.choice(['flu', 'COVID-19', 'foodborne illness', 'allergies']),
        action=random.choice(['vaccination', 'regular screening', 'lifestyle changes']),
        phase=random.choice(['1', '2', '3']),
        food=random.choice(['coffee', 'dark chocolate', 'nuts', 'fish']),
        exercise=random.choice(['HIIT', 'yoga', 'pilates', 'strength training']),
        benefit=random.choice(['weight loss', 'mental health', 'cardiovascular health']),
        technology=random.choice(['AI diagnostic system', 'robotic surgery', 'telemedicine platform']),
        condition=random.choice(['heart disease', 'diabetes', 'obesity', 'depression']),
        celebrity=random.choice(['Emma Stone', 'Ryan Gosling', 'Zendaya', 'Timothée Chalamet']),
        award=random.choice(['Oscar', 'Grammy', 'Emmy', 'Golden Globe']),
        work=random.choice(['performance', 'album', 'film', 'series']),
        genre=random.choice(['sci-fi', 'drama', 'comedy', 'action']),
        title=random.choice(['Starlight', 'Echoes', 'The Journey', 'Beyond']),
        artist=random.choice(['Taylor Swift', 'Beyoncé', 'Drake', 'Adele']),
        artist2=random.choice(['Ed Sheeran', 'The Weeknd', 'Billie Eilish']),
        number=random.randint(10, 100),
        platform=random.choice(['Netflix', 'Disney+', 'HBO Max', 'Prime Video']),
        show=random.choice(['new series', 'documentary', 'limited series']),
        aspect=random.choice(['storytelling', 'performances', 'production quality']),
        product=random.choice(['fashion', 'beauty', 'lifestyle', 'fragrance']),
        game=random.choice(['Fortnite', 'Minecraft', 'Call of Duty', 'League of Legends'])
    )
    
    return article

def generate_dataset(num_articles=1000):
    """Generate a large dataset of news articles"""
    categories = list(NEWS_TEMPLATES.keys())
    articles_per_category = num_articles // len(categories)
    
    data = []
    dates = [datetime.now() - timedelta(days=random.randint(1, 365)) for _ in range(num_articles)]
    
    for category in categories:
        for i in range(articles_per_category):
            content = generate_news_article(category)
            title = content[:60] + "..." if len(content) > 60 else content
            
            data.append({
                'title': title,
                'content': content,
                'category': category,
                'date': dates[len(data)].strftime('%Y-%m-%d'),
                'source': random.choice(['Reuters', 'AP', 'BBC', 'CNN', 'Bloomberg', 'WSJ', 'NYT'])
            })
    
    # Add remaining articles to balance
    remaining = num_articles - len(data)
    for _ in range(remaining):
        category = random.choice(categories)
        content = generate_news_article(category)
        title = content[:60] + "..." if len(content) > 60 else content
        
        data.append({
            'title': title,
            'content': content,
            'category': category,
            'date': dates[len(data)].strftime('%Y-%m-%d'),
            'source': random.choice(['Reuters', 'AP', 'BBC', 'CNN', 'Bloomberg', 'WSJ', 'NYT'])
        })
    
    return pd.DataFrame(data)

if __name__ == "__main__":
    print("Generating 1,000 realistic news articles...")
    df = generate_dataset(1000)
    
    output_path = "news_agent/data/mdpi_news.csv"
    df.to_csv(output_path, index=False)
    
    print(f"✅ Generated {len(df)} articles")
    print(f"✅ Saved to {output_path}")
    print(f"✅ Categories: {df['category'].value_counts().to_dict()}")
    print(f"✅ File size: {len(df) * df.memory_usage(deep=True).sum() / 1024 / 1024:.2f} MB (in memory)")

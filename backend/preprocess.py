"""
Preprocessing module for job description and CV text processing
"""
from typing import List, Tuple
from nb_loader import basic_clean, tokenize_lemmatize
from rapidfuzz import process, fuzz
import re


def clean_for_model(text: str) -> str:
    """
    Clean text for model processing
    Combines basic cleaning and tokenization/lemmatization
    """
    if not text or not isinstance(text, str):
        return ""
    
    # Apply basic cleaning
    cleaned = basic_clean(text, remove_digits=False)
    
    # Apply tokenization and lemmatization
    processed = tokenize_lemmatize(cleaned, min_len=2)
    
    return processed


def extract_keywords(jd_text: str, cv_text: str, topk: int = 6) -> List[str]:
    """
    Extract matching keywords/skills between JD and CV
    Uses rapidfuzz to find similar phrases and terms
    """
    if not jd_text or not cv_text:
        return []
    
    # Clean both texts
    jd_clean = clean_for_model(jd_text)
    cv_clean = clean_for_model(cv_text)
    
    if not jd_clean or not cv_clean:
        return []
    
    # Split into words and phrases
    jd_words = jd_clean.split()
    cv_words = cv_clean.split()
    
    # Create n-grams for better phrase matching
    jd_phrases = []
    cv_phrases = []
    
    # Add individual words
    jd_phrases.extend(jd_words)
    cv_phrases.extend(cv_words)
    
    # Add bigrams
    for i in range(len(jd_words) - 1):
        jd_phrases.append(f"{jd_words[i]} {jd_words[i+1]}")
    for i in range(len(cv_words) - 1):
        cv_phrases.append(f"{cv_words[i]} {cv_words[i+1]}")
    
    # Add trigrams
    for i in range(len(jd_words) - 2):
        jd_phrases.append(f"{jd_words[i]} {jd_words[i+1]} {jd_words[i+2]}")
    for i in range(len(cv_words) - 2):
        cv_phrases.append(f"{cv_words[i]} {cv_words[i+1]} {cv_words[i+2]}")
    
    # Find matches using rapidfuzz
    matches = []
    for jd_phrase in jd_phrases:
        if len(jd_phrase.strip()) < 3:  # Skip very short phrases
            continue
            
        # Find best match in CV
        best_match = process.extractOne(
            jd_phrase, 
            cv_phrases, 
            scorer=fuzz.ratio,
            score_cutoff=70  # Minimum similarity threshold
        )
        
        if best_match:
            matches.append((jd_phrase, best_match[1]))
    
    # Sort by similarity score and return top matches
    matches.sort(key=lambda x: x[1], reverse=True)
    
    # Extract unique keywords, avoiding duplicates
    keywords = []
    seen = set()
    for phrase, score in matches[:topk*2]:  # Get more to filter duplicates
        phrase_lower = phrase.lower()
        if phrase_lower not in seen and len(phrase.strip()) >= 3:
            keywords.append(phrase)
            seen.add(phrase_lower)
            if len(keywords) >= topk:
                break
    
    return keywords


def extract_skills_from_text(text: str) -> List[str]:
    """
    Extract potential skills from text using common patterns
    """
    if not text:
        return []
    
    # Common skill patterns
    skill_patterns = [
        r'\b(?:python|java|javascript|react|angular|vue|node\.?js|express|django|flask|spring|laravel|php|ruby|rails|go|rust|c\+\+|c#|swift|kotlin|scala|r|matlab|sql|mysql|postgresql|mongodb|redis|elasticsearch|aws|azure|gcp|docker|kubernetes|jenkins|git|github|gitlab|jira|confluence|agile|scrum|devops|ci/cd|microservices|api|rest|graphql|grpc|tensorflow|pytorch|pandas|numpy|scikit-learn|opencv|pytorch|keras|spark|hadoop|kafka|rabbitmq|nginx|apache|linux|ubuntu|centos|windows|macos|ios|android|flutter|react native|xamarin|cordova|ionic|bootstrap|tailwind|sass|less|webpack|babel|typescript|es6|html5|css3|json|xml|yaml|toml|ini|bash|powershell|python|r|sql|nosql|machine learning|deep learning|artificial intelligence|data science|data analysis|statistics|mathematics|algorithms|data structures|software engineering|web development|mobile development|backend development|frontend development|full stack|cloud computing|cybersecurity|blockchain|ethereum|bitcoin|solidity|web3|defi|nft|metaverse|ar|vr|iot|embedded systems|firmware|hardware|electronics|robotics|automation|testing|qa|quality assurance|unit testing|integration testing|end-to-end testing|performance testing|security testing|penetration testing|vulnerability assessment|risk management|compliance|gdpr|hipaa|sox|pci|iso|audit|governance|project management|product management|business analysis|requirements gathering|stakeholder management|agile|scrum|kanban|lean|six sigma|pmp|prince2|itil|cobit|togaf|zachman|enterprise architecture|solution architecture|system design|database design|network design|security architecture|cloud architecture|microservices architecture|event-driven architecture|domain-driven design|test-driven development|behavior-driven development|continuous integration|continuous deployment|continuous delivery|infrastructure as code|configuration management|monitoring|logging|alerting|observability|apm|splunk|datadog|newrelic|grafana|prometheus|elk stack|elasticsearch|logstash|kibana|fluentd|fluentbit|vector|jaeger|zipkin|opentelemetry|distributed tracing|service mesh|istio|linkerd|consul|vault|etcd|zookeeper|kafka|pulsar|rabbitmq|activemq|redis|memcached|hazelcast|ignite|cassandra|dynamodb|couchdb|neo4j|arangodb|orientdb|influxdb|timescaledb|clickhouse|bigquery|redshift|snowflake|databricks|hive|presto|trino|druid|pinot|kylin|superset|metabase|tableau|power bi|qlik|looker|mode|periscope|chartio|plotly|d3\.js|observable|jupyter|zeppelin|rstudio|spyder|pycharm|vscode|intellij|eclipse|netbeans|vim|emacs|sublime|atom|brackets|webstorm|phpstorm|rubymine|clion|appcode|datagrip|pycharm|rider|resharper|dotcover|dotmemory|dotpeek|dotnet|core|framework|standard|maui|blazor|wpf|winforms|wcf|web api|mvc|mvp|mvvm|clean architecture|onion architecture|hexagonal architecture|cqs|cqrs|event sourcing|saga pattern|repository pattern|unit of work|factory pattern|builder pattern|singleton pattern|observer pattern|strategy pattern|command pattern|adapter pattern|facade pattern|proxy pattern|decorator pattern|bridge pattern|composite pattern|flyweight pattern|template method pattern|visitor pattern|iterator pattern|mediator pattern|memento pattern|state pattern|chain of responsibility pattern|interpreter pattern|null object pattern|specification pattern|value object pattern|entity pattern|aggregate pattern|domain service pattern|application service pattern|infrastructure service pattern|presentation service pattern|business service pattern|data access object pattern|data transfer object pattern|view object pattern|model view controller pattern|model view presenter pattern|model view viewmodel pattern|presentation model pattern|supervising controller pattern|passive view pattern|humble dialog pattern|model view controller pattern|model view presenter pattern|model view viewmodel pattern|presentation model pattern|supervising controller pattern|passive view pattern|humble dialog pattern)\b',
        r'\b(?:bachelor|master|phd|doctorate|degree|certification|certified|license|diploma|certificate|course|training|workshop|seminar|conference|meetup|hackathon|bootcamp|internship|apprenticeship|mentorship|coaching|consulting|freelancing|contracting|remote|onsite|hybrid|full-time|part-time|contract|permanent|temporary|intern|junior|mid-level|senior|lead|principal|architect|manager|director|vp|cto|ceo|founder|co-founder|entrepreneur|startup|scaleup|enterprise|fortune 500|unicorn|ipo|acquisition|merger|partnership|collaboration|team|squad|tribe|guild|chapter|community|network|ecosystem|platform|marketplace|saas|paas|iaas|serverless|edge computing|quantum computing|5g|6g|wifi|bluetooth|nfc|rfid|gps|gis|gis|gps|location|geospatial|mapping|cartography|surveying|photogrammetry|lidar|radar|sonar|ultrasound|infrared|thermal|optical|laser|led|oled|lcd|crt|plasma|projector|display|screen|monitor|tv|smart tv|streaming|video|audio|sound|music|podcast|radio|broadcast|telecom|telecommunications|networking|routing|switching|firewall|vpn|proxy|load balancer|cdn|dns|dhcp|tcp|udp|http|https|ftp|sftp|ssh|telnet|snmp|smtp|pop|imap|ldap|kerberos|oauth|saml|jwt|jwe|jws|jwk|pkcs|x509|pki|ca|certificate authority|digital signature|encryption|decryption|hashing|salting|bcrypt|scrypt|argon2|pbkdf2|rsa|aes|des|3des|blowfish|twofish|serpent|camellia|chacha20|poly1305|gcm|ccm|ocb|eax|siv|ctr|cbc|cfb|ofb|ecb|gcm|ccm|ocb|eax|siv|ctr|cbc|cfb|ofb|ecb)\b'
    ]
    
    skills = []
    text_lower = text.lower()
    
    for pattern in skill_patterns:
        matches = re.findall(pattern, text_lower, re.IGNORECASE)
        skills.extend(matches)
    
    # Remove duplicates and return unique skills
    return list(set(skills))


def preprocess_text_pipeline(text: str) -> Tuple[str, List[str]]:
    """
    Complete preprocessing pipeline for text
    Returns cleaned text and extracted skills
    """
    cleaned = clean_for_model(text)
    skills = extract_skills_from_text(text)
    
    return cleaned, skills

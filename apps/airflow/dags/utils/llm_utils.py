"""
LLM utilities for generating email content using OpenAI.
Handles prompt generation and API calls for email content creation.
"""

import os
import openai
from typing import List, Dict, Any
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class EmailContentGenerator:
    """Email content generator using OpenAI GPT models."""
    
    def __init__(self, api_key: str = None, model: str = "gpt-3.5-turbo"):
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OpenAI API key not provided")
        
        self.model = model
        self.client = openai.OpenAI(api_key=self.api_key)
    
    def generate_email_content(self, articles: List[Dict[str, Any]]) -> Dict[str, str]:
        """Generate email subject and HTML body from articles."""
        
        if not articles:
            return {
                'subject': 'Resumo Diário de Notícias - Sem Artigos',
                'content': '<html><body><h1>Nenhum artigo encontrado hoje.</h1></body></html>'
            }
        
        # Prepare articles data for prompt
        articles_text = self._prepare_articles_for_prompt(articles)
        
        # Generate subject
        subject = self._generate_subject(len(articles))
        
        # Generate HTML content
        content = self._generate_html_content(articles_text, articles)
        
        return {
            'subject': subject,
            'content': content
        }
    
    def _prepare_articles_for_prompt(self, articles: List[Dict[str, Any]]) -> str:
        """Prepare articles data for the prompt."""
        articles_text = ""
        
        for i, article in enumerate(articles, 1):
            title = article.get('title', 'Sem título')
            content = article.get('content', 'Sem conteúdo')
            url = article.get('url', '#')
            
            # Truncate content if too long
            if len(content) > 500:
                content = content[:500] + "..."
            
            articles_text += f"""
Artigo {i}:
Título: {title}
URL: {url}
Conteúdo: {content}
---
"""
        
        return articles_text
    
    def _generate_subject(self, article_count: int) -> str:
        """Generate email subject line."""
        today = datetime.now().strftime('%d/%m/%Y')
        return f'Resumo Diário de Notícias - {article_count} artigos - {today}'
    
    def _generate_html_content(self, articles_text: str, articles: List[Dict[str, Any]]) -> str:
        """Generate HTML email content using LLM for summary."""
        
        # Generate summary using LLM
        summary = self._generate_summary(articles_text)
        
        # Build HTML email
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }}
        h1 {{
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }}
        h2 {{
            color: #2980b9;
            margin-top: 30px;
        }}
        .summary {{
            background-color: #ecf0f1;
            padding: 20px;
            border-radius: 5px;
            margin: 20px 0;
        }}
        .article {{
            background-color: #fff;
            border-left: 4px solid #3498db;
            padding: 15px;
            margin: 15px 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .article h3 {{
            margin-top: 0;
            color: #2c3e50;
        }}
        .article-link {{
            color: #3498db;
            text-decoration: none;
            font-weight: bold;
        }}
        .article-link:hover {{
            text-decoration: underline;
        }}
        .footer {{
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #bdc3c7;
            color: #7f8c8d;
            font-size: 0.9em;
        }}
    </style>
</head>
<body>
    <h1>Resumo Diário de Notícias</h1>
    <p><strong>Data:</strong> {datetime.now().strftime('%d/%m/%Y')}</p>
    <p><strong>Total de Artigos:</strong> {len(articles)}</p>
    
    <div class="summary">
        <h2>Resumo Executivo</h2>
        {summary}
    </div>
    
    <h2>Artigos do Dia</h2>
"""
        
        # Add articles
        for i, article in enumerate(articles, 1):
            title = article.get('title', 'Sem título')
            content = article.get('content', 'Sem conteúdo')
            url = article.get('url', '#')
            
            # Truncate content for email
            if len(content) > 300:
                content = content[:300] + "..."
            
            html += f"""
    <div class="article">
        <h3>{i}. {title}</h3>
        <p>{content}</p>
        <p><a href="{url}" class="article-link">Ler artigo completo &rarr;</a></p>
    </div>
"""
        
        # Add footer
        html += """
    <div class="footer">
        <p>Este é um resumo automático gerado pelo sistema de agregação de notícias.</p>
    </div>
</body>
</html>
"""
        
        return html
    
    def _generate_summary(self, articles_text: str) -> str:
        """Generate executive summary using LLM."""
        
        prompt = f"""
Analise as seguintes notícias e crie um resumo executivo em formato de texto contínuo.

Instruções:
1. Identifique os temas principais
2. Destaque tendências importantes
3. Mantenha o resumo entre 150-200 palavras
4. Use linguagem profissional e clara
5. Estruture em parágrafos curtos de texto corrido
6. NÃO use bullet points, listas ou marcadores
7. Escreva em prosa contínua, como um texto narrativo

Notícias:
{articles_text}

Gere o resumo executivo em HTML formatado usando apenas tags <p> para parágrafos (não use listas <ul>, <ol> ou <li>):
"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "Você é um analista financeiro que cria resumos executivos de notícias em formato de texto contínuo. Sempre escreva em prosa narrativa usando parágrafos, nunca use bullet points ou listas."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=500,
                temperature=0.3
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"Error generating summary: {e}")
            return f"<p>Erro ao gerar resumo: {str(e)}</p>"

# Global generator instance
def get_email_generator() -> EmailContentGenerator:
    """Get configured email content generator."""
    return EmailContentGenerator()

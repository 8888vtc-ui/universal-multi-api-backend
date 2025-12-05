"""
Course Generator - Génération automatique de cours vidéo
"""
from typing import Dict, Any, List
from services.ai_router import ai_router
from services.video.video_router import video_router
import asyncio


class CourseGenerator:
    """Générateur de cours vidéo automatique"""
    
    def __init__(self):
        self.ai_router = ai_router
        self.video_router = video_router
    
    async def generate_course(
        self,
        topic: str,
        duration_minutes: int = 5,
        language: str = "fr",
        avatar_id: str = "anna",
        include_quiz: bool = True
    ) -> Dict[str, Any]:
        """
        Générer un cours complet automatiquement
        
        Args:
            topic: Sujet du cours
            duration_minutes: Durée souhaitée (détermine le nombre de sections)
            language: Langue du cours
            avatar_id: Avatar à utiliser
            include_quiz: Inclure un quiz à la fin
        
        Returns:
            Dict avec sections, vidéos, quiz, etc.
        """
        # 1. Générer le contenu du cours avec IA
        course_content = await self._generate_course_content(
            topic=topic,
            duration_minutes=duration_minutes,
            language=language
        )
        
        # 2. Diviser en sections (chacune ~30 secondes)
        sections = course_content.get("sections", [])
        
        # 3. Générer les vidéos pour chaque section
        video_tasks = []
        for i, section in enumerate(sections, 1):
            video_task = self._generate_section_video(
                section_text=section.get("content", ""),
                section_number=i,
                total_sections=len(sections),
                avatar_id=avatar_id,
                language=language
            )
            video_tasks.append((section, video_task))
        
        # Générer toutes les vidéos en parallèle
        section_videos = []
        for section, video_task in video_tasks:
            try:
                video_result = await video_task
                section_videos.append({
                    "section": section,
                    "video": video_result
                })
            except Exception as e:
                print(f"Error generating video for section: {e}")
                section_videos.append({
                    "section": section,
                    "video": None,
                    "error": str(e)
                })
        
        # 4. Générer quiz si demandé
        quiz = None
        if include_quiz:
            quiz = await self._generate_quiz(
                topic=topic,
                content=course_content,
                language=language
            )
        
        return {
            "course_id": f"course_{topic.lower().replace(' ', '_')}",
            "topic": topic,
            "language": language,
            "duration_minutes": duration_minutes,
            "sections": section_videos,
            "quiz": quiz,
            "total_sections": len(sections),
            "status": "completed"
        }
    
    async def _generate_course_content(
        self,
        topic: str,
        duration_minutes: int,
        language: str
    ) -> Dict[str, Any]:
        """Générer le contenu du cours avec IA"""
        sections_count = max(2, duration_minutes * 2)  # ~30 sec par section
        
        prompt = f"""
        Crée un cours sur le sujet : "{topic}"
        
        Langue : {language}
        Durée : {duration_minutes} minutes
        Nombre de sections : {sections_count}
        
        Chaque section doit :
        - Être claire et concise (~30 secondes de lecture)
        - Être adaptée à un format vidéo
        - Suivre logiquement la section précédente
        
        Format de réponse JSON :
        {{
            "title": "Titre du cours",
            "introduction": "Introduction courte",
            "sections": [
                {{
                    "number": 1,
                    "title": "Titre section",
                    "content": "Contenu de la section (texte à prononcer)"
                }}
            ],
            "conclusion": "Conclusion du cours"
        }}
        
        Réponds UNIQUEMENT en JSON valide, sans markdown.
        """
        
        try:
            response = await self.ai_router.chat(prompt, max_tokens=2000)
            content = response.get("content", "")
            
            # Parser le JSON (peut être dans des blocs markdown)
            import json
            import re
            
            # Extraire JSON si dans markdown
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                content = json_match.group(0)
            
            course_data = json.loads(content)
            return course_data
        
        except Exception as e:
            # Fallback : créer un cours simple
            return {
                "title": f"Cours sur {topic}",
                "introduction": f"Bienvenue dans ce cours sur {topic}.",
                "sections": [
                    {
                        "number": 1,
                        "title": "Introduction",
                        "content": f"Dans ce cours, nous allons découvrir {topic}."
                    },
                    {
                        "number": 2,
                        "title": "Conclusion",
                        "content": f"Merci d'avoir suivi ce cours sur {topic}."
                    }
                ],
                "conclusion": "Fin du cours."
            }
    
    async def _generate_section_video(
        self,
        section_text: str,
        section_number: int,
        total_sections: int,
        avatar_id: str,
        language: str
    ) -> Dict[str, Any]:
        """Générer une vidéo pour une section"""
        # Ajouter numéro de section au texte
        text = f"Section {section_number} sur {total_sections}. {section_text}"
        
        # Limiter à 500 caractères
        if len(text) > 500:
            text = text[:497] + "..."
        
        result = await self.video_router.create_talking_avatar(
            text=text,
            avatar_id=avatar_id,
            language=language,
            use_free=False
        )
        
        return result
    
    async def _generate_quiz(
        self,
        topic: str,
        content: Dict[str, Any],
        language: str
    ) -> Dict[str, Any]:
        """Générer un quiz basé sur le contenu du cours"""
        sections_text = "\n".join([
            f"Section {s.get('number')}: {s.get('title')} - {s.get('content', '')[:100]}"
            for s in content.get("sections", [])
        ])
        
        prompt = f"""
        Crée un quiz de 5 questions sur le cours suivant :
        
        Sujet : {topic}
        
        Contenu :
        {sections_text}
        
        Format JSON :
        {{
            "questions": [
                {{
                    "question": "Question",
                    "options": ["Option 1", "Option 2", "Option 3", "Option 4"],
                    "correct": 0
                }}
            ]
        }}
        
        Réponds UNIQUEMENT en JSON valide.
        """
        
        try:
            response = await self.ai_router.chat(prompt, max_tokens=1000)
            content_text = response.get("content", "")
            
            import json
            import re
            
            json_match = re.search(r'\{.*\}', content_text, re.DOTALL)
            if json_match:
                content_text = json_match.group(0)
            
            quiz_data = json.loads(content_text)
            return quiz_data
        
        except Exception as e:
            # Fallback : quiz simple
            return {
                "questions": [
                    {
                        "question": f"Qu'avez-vous appris sur {topic} ?",
                        "options": ["Beaucoup", "Un peu", "Rien", "Je ne sais pas"],
                        "correct": 0
                    }
                ]
            }


# Singleton instance
course_generator = CourseGenerator()



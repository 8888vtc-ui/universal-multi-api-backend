"""
📊 DATA AGENT
Expert in data analysis, processing, and machine learning.
Uses GPT-4o for complex data reasoning.
"""
from typing import Dict, Any, List
from .base_agent import BaseAgent


class DataAgent(BaseAgent):
    """Expert in data analysis and machine learning"""
    
    def __init__(self):
        super().__init__(
            name="📊 Data Agent",
            model="gpt-4o",
            role="Analyse les données, crée des modèles ML, génère des insights"
        )
    
    async def _do_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        action = task.get("action", "analyze_data")
        
        actions = {
            "analyze_data": self._analyze_data,
            "create_model": self._create_model,
            "feature_engineering": self._feature_engineering,
            "exploratory_analysis": self._exploratory_analysis,
            "predict": self._predict,
            "generate_report": self._generate_report,
            "clean_data": self._clean_data,
            "visualize": self._visualize,
        }
        
        handler = actions.get(action)
        if handler:
            return await handler(task)
        else:
            return {"success": False, "error": f"Unknown action: {action}"}
    
    async def _analyze_data(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze dataset and provide insights"""
        data_description = task.get("data", "")
        columns = task.get("columns", [])
        sample = task.get("sample", "")
        
        prompt = f"""
        Analyse ce dataset:
        
        Description: {data_description}
        Colonnes: {columns}
        Échantillon: {sample}
        
        Analyse:
        1. **STRUCTURE**
           - Types de données
           - Valeurs manquantes
           - Cardinalité
        
        2. **STATISTIQUES**
           - Mesures centrales (mean, median, mode)
           - Dispersion (std, variance, range)
           - Distribution
        
        3. **CORRÉLATIONS**
           - Corrélations fortes
           - Variables redondantes
        
        4. **ANOMALIES**
           - Outliers
           - Inconsistances
        
        5. **INSIGHTS**
           - Patterns identifiés
           - Hypothèses à tester
           - Recommandations
        
        Format: Rapport structuré avec visualisations suggérées
        """
        result = await self.think(prompt)
        return {"success": True, "analysis": result}
    
    async def _create_model(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Create machine learning model"""
        problem_type = task.get("problem_type", "classification")
        target = task.get("target", "")
        features = task.get("features", [])
        
        prompt = f"""
        Crée un modèle ML:
        
        Type: {problem_type}
        Target: {target}
        Features: {features}
        
        Pipeline complète:
        
        1. **PREPROCESSING**
           - Encodage catégoriel
           - Normalisation
           - Feature selection
        
        2. **MODÈLE**
           - Algorithme recommandé
           - Hyperparamètres
           - Cross-validation
        
        3. **ÉVALUATION**
           - Métriques appropriées
           - Baseline
           - Interprétabilité
        
        4. **CODE**
           - Code Python complet (sklearn/pytorch)
           - Pipeline de prédiction
           - Sauvegarde/chargement modèle
        
        Format: Code Python avec explications
        """
        result = await self.think(prompt)
        return {"success": True, "model": result, "problem_type": problem_type}
    
    async def _feature_engineering(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Generate feature engineering ideas"""
        columns = task.get("columns", [])
        domain = task.get("domain", "")
        
        prompt = f"""
        Feature engineering pour:
        
        Colonnes: {columns}
        Domaine: {domain}
        
        Suggestions:
        1. **TRANSFORMATIONS**
           - Log, sqrt, box-cox
           - Binning
           - Polynomial features
        
        2. **CRÉATION**
           - Ratios
           - Agrégations
           - Interactions
        
        3. **TEMPORELLES** (si applicable)
           - Lag features
           - Rolling statistics
           - Seasonal decomposition
        
        4. **TEXTUELLES** (si applicable)
           - TF-IDF
           - Embeddings
           - N-grams
        
        Pour chaque feature:
        - Nom et formule
        - Justification
        - Impact attendu
        """
        result = await self.think(prompt)
        return {"success": True, "features": result}
    
    async def _exploratory_analysis(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Perform exploratory data analysis"""
        data = task.get("data", "")
        questions = task.get("questions", [])
        
        prompt = f"""
        Analyse exploratoire:
        
        Data: {data}
        Questions: {questions}
        
        EDA complète:
        1. **UNIVARIATE**
           - Distribution de chaque variable
           - Histogrammes, box plots
        
        2. **BIVARIATE**
           - Relations entre variables
           - Scatter plots, heatmaps
        
        3. **MULTIVARIATE**
           - PCA, clustering
           - Patterns complexes
        
        4. **HYPOTHÈSES**
           - Tests statistiques
           - Intervalles de confiance
        
        Code Python pour générer les visualisations.
        """
        result = await self.think(prompt)
        return {"success": True, "eda": result}
    
    async def _predict(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Make predictions and explain them"""
        model_type = task.get("model_type", "")
        input_data = task.get("input_data", {})
        
        prompt = f"""
        Prédiction avec:
        
        Modèle: {model_type}
        Données d'entrée: {input_data}
        
        Fournis:
        1. Prédiction
        2. Probabilité/Confiance
        3. Explication (feature importance, SHAP)
        4. Incertitude
        5. Recommandations basées sur la prédiction
        """
        result = await self.think(prompt)
        return {"success": True, "prediction": result}
    
    async def _generate_report(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Generate data analysis report"""
        analysis_results = task.get("results", {})
        audience = task.get("audience", "technical")
        
        prompt = f"""
        Génère un rapport d'analyse pour audience {audience}:
        
        Résultats: {analysis_results}
        
        Structure:
        1. Executive Summary
        2. Méthodologie
        3. Findings principaux
        4. Visualisations clés
        5. Recommendations
        6. Next steps
        
        Adapte le langage au niveau {audience}.
        """
        result = await self.think(prompt)
        return {"success": True, "report": result, "audience": audience}
    
    async def _clean_data(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Generate data cleaning code"""
        issues = task.get("issues", [])
        columns = task.get("columns", [])
        
        prompt = f"""
        Code de nettoyage de données:
        
        Problèmes: {issues}
        Colonnes: {columns}
        
        Opérations:
        1. Valeurs manquantes (imputation)
        2. Duplicates
        3. Outliers
        4. Types incorrects
        5. Inconsistances
        6. Standardisation
        
        Code Python (pandas) avec explications.
        """
        result = await self.think(prompt)
        return {"success": True, "cleaning_code": result}
    
    async def _visualize(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Generate visualization code"""
        data_type = task.get("data_type", "")
        viz_type = task.get("viz_type", "")
        
        prompt = f"""
        Génère du code de visualisation:
        
        Type de données: {data_type}
        Type de visualisation: {viz_type}
        
        Génère du code Python (matplotlib/seaborn/plotly) pour:
        - Visualisation professionnelle
        - Couleurs appropriées
        - Labels lisibles
        - Légende
        - Export haute résolution
        
        Plusieurs options de visualisation si pertinent.
        """
        result = await self.think(prompt)
        return {"success": True, "viz_code": result}

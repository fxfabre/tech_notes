Insert d'un CSV dans BQ
- Ne pas essayer de convertir en int une colonne d'une dataframe :
  Le format int ne sait pas gérer les nan / valeurs manquantes  
  -> Intégrer en float + appliquer un cast en SQL

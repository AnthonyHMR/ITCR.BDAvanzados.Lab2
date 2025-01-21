CALL apoc.periodic.iterate(
  "LOAD CSV WITH HEADERS FROM 'file:///netflix_disney.csv' AS row RETURN row",
  "
  MERGE (s:Show { show_id: row.show_id })
  SET 
      s.title        = row.title,
      s.type         = row.type,
      s.date_added   = row.date_added,
      s.release_year = toInteger(row.release_year),
      s.rating       = row.rating,
      s.duration     = row.duration,
      s.description  = row.description
  
  FOREACH (dir IN CASE 
                  WHEN row.director IS NOT NULL AND row.director <> '' 
                  THEN split(row.director, ',') 
                  ELSE [] 
                END | 
      MERGE (d:Director { name: trim(dir) })
      MERGE (s)-[:DIRECTED_BY]->(d)
  )

  FOREACH (actor IN CASE 
                   WHEN row.cast IS NOT NULL AND row.cast <> '' 
                   THEN split(row.cast, ',') 
                   ELSE [] 
                   END |
      MERGE (a:Actor { name: trim(actor) })
      MERGE (s)-[:CAST_MEMBER]->(a)
  )

  FOREACH (cn IN CASE
                 WHEN row.country IS NOT NULL AND row.country <> ''
                 THEN split(row.country, ',')
                 ELSE []
                 END |
      MERGE (c:Country { name: trim(cn) })
      MERGE (s)-[:AVAILABLE_IN]->(c)
  )

  FOREACH (gen IN CASE
                  WHEN row.listed_in IS NOT NULL AND row.listed_in <> ''
                  THEN split(row.listed_in, ',')
                  ELSE []
                  END |
      MERGE (g:Genre { name: trim(gen) })
      MERGE (s)-[:HAS_GENRE]->(g)
  )
  ",
  {batchSize:1000, iterateList:true, parallel:false}
)
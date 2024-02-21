# Función que filtra del dataset según el año de adquisición de la obra
def apply_accession_filter(df, adquisicion_slider):
    df = df[df['accessionYear']>= adquisicion_slider]
    return df

#Función que filtra del dataset según si se desean excluir las obras destacadas o no destacadas
def apply_highlight_filter(df, get_highlight):
    if get_highlight=='Destacadas':
        df = df[df['isHighlight'] == True]
    elif get_highlight=='No Destacadas':
        df = df[df['isHighlight']== False]
    return df

# Función que filtra el dataset según si se desean excluir las obras de dominio público o protegidas por derechos de autor
def apply_license_filter(df, get_license):
    if get_license=='Dominio Público':
        df = df[df['isPublicDomain'] == True]
    elif get_license=='Protegidas por derechos de autor':
        df = df[df['isPublicDomain']== False]
    return df

# Función que filtra el dataset según el departamento
def apply_department_filter(df, department_options):
    if isinstance(department_options, list): 
        df = df[df['department'].isin(department_options)]
    else:
        df = df[df['department'] == department_options]
    return df

# Función que filtra del dataset según si se desean excluir artistas anónimos o desconocidos
def apply_anonymous_filter(df, exclude_unknown, column):
    if exclude_unknown:
        df = df[~df[column].str.contains('anonymous|unknown|unidentified', case=False)]
    return df
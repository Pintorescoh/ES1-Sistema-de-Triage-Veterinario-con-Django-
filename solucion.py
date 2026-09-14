def decidir(dificultad_respiratoria, nivel_dolor):
    # 2. Motor de Decisiones (Triage) extraído de tu código original
    if dificultad_respiratoria not in [0, 1] or nivel_dolor < 1 or nivel_dolor > 10:
        return "Inválido"
    elif dificultad_respiratoria == 1:
        return "Código Rojo"
    elif nivel_dolor >= 6:
        return "Código Amarillo"
    else:
        return "Código Verde"
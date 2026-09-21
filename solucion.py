def normalizar_gravedad(valor):
    if valor is None:
        return ""
    texto = str(valor).strip()
    if texto.lower().startswith("código "):
        return texto.replace("Código ", "", 1).strip()
    return texto


def decidir(dificultad_respiratoria, nivel_dolor):
    # Motor de decisiones del triage.
    if dificultad_respiratoria not in [0, 1] or nivel_dolor < 0 or nivel_dolor > 10:
        return "Inválido"
    elif dificultad_respiratoria == 1:
        return "Rojo"
    elif nivel_dolor >= 6:
        return "Amarillo"
    else:
        return "Verde"
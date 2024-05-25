# Variáveis
PYTHON=python3
FILE=DashboardProcessBF.py
RUN_COMMAND=$(PYTHON) $(FILE)

# Regra padrão
.DEFAULT_GOAL := run

# Regras
.PHONY: run
run:
	$(RUN_COMMAND)

.PHONY: clean
clean:
    # Não há arquivos temporários para limpar


# Alvin

Alvin (Assistente de Localização e Vigilância sobre Incidentes Naturais) é um chatbot caracterizado como um adorável cachorro caramelo disponibilizado no Telegram cuja função é auxiliar pessoas procurando ajuda e pessoas procurando ajudar em cenários de incidentes naturais, como a histórica enchente do Rio Grande do Sul de 2024. 

O Alvin é equipado com conversação baseada em Large Language Models e é capaz de acessar informações como abrigos que estão recebendos doações e/ou pessoas, encontrar pontos de recolhimento de recursos e abrigos próximos ao usuário, alertas da Defesa Civil, entre outros.

## Arquitetura
O projeto foi desenvolvido usando a arquitetura de micro-serviços visando modularizar as funcionalidades da aplicação para facilitar a manutenção do código. Nesta versão, utilizamos o Google Gemini Language para gerenciar as conversas do chat, o Google Gemini Vision para extrair informações de imagens de banners de alerta postados no site da Defesa Civil do Rio Grande do Sul, ambos modelos empacotados pelo LangChain. Por fim, usamos o Telegram BotFather como interface com o usuário final.

Estas ferramentas podem ser substituídas por outras similares, como os modelos generativos da OpenAI, e o WhatsApp.

### Considerações

Esse projeto é um protótipo. Para desenvolve-lo as seguintes considerações foram feitas:

1. O banco de dados de centro de doações, abrigos e entidades é gerido por um órgão oficial e acessado via API request externo. Esse banco de dados deve validar informações, ser robusto e verídico, a API externa não passará informações pessoais e não públicas e respeitará a LGPD
    - Neste protótipo, os dados relacionados a abrigos e centro de doações são mockados. Recomendamos que seja feita uma conexão direta com um banco de dados unificado para que o modelo tenha informações atualizadas.
2. Os alertas publicados no site da Defesa Civil do Rio Grande do Sul são verídicos e atualizados com frequência.
    - Para essa funcionalidade, usamos apenas o site da Defesa Civil do estado do Rio Grande do Sul é monitorado. Ela pode ser ativada para atualizar as informações em uma cadência específica (por exemplo, a cada 15 minutos), mas recomendamos a integração com uma plataforma unificada para abranger todo o território nacional.

### Funcionalidades

O Alvin Bot pode ser utilizado por dois tipos de usuários diferentes e pode realizar as seguintes tarefas:

1. Quem gostaria de ajudar
    - Alvin pode direcionar doações para o lugar mais próximo
    - Alvin pode confirmar chaves Pix de entidades cadastradas
2. Quem precisa de ajuda
    - Alvin pode acionar a defesa civil
    - Alvin pode buscar abrigos próximos
    - Alvin pode buscar centros de distribuição de doações próximos e cadastrados
    - Alvin pode pesquisar alertas correntes para o estado do Rio Grande do Sul

### Estrutura

```
📦alvinbot
 ┣ 📂data
 ┃ ┗ 📂tables
 ┃ ┃ ┣ 📜entidades.json
 ┃ ┃ ┣ 📜Mock_Abrigos.xlsx
 ┃ ┃ ┣ 📜Mock_CentroDeDoacoes.xlsx
 ┃ ┃ ┣ 📜Mock_Entidades.xlsx
 ┃ ┃ ┣ 📜Mock_LotacaoDosAbrigos.xlsx
 ┃ ┃ ┣ 📜Mock_Ocorrencias.xlsx
 ┃ ┃ ┣ 📜Mock_RequisicaoDeDoacoes.xlsx
 ┃ ┃ ┣ 📜Mock_RequisicaoVoluntarios.xlsx
 ┃ ┃ ┗ 📜Real_ListaDeAlertasEmRS.csv
 ┣ 📂services
 ┃ ┣ 📂alert
 ┃ ┃ ┣ 📂tests
 ┃ ┃ ┃ ┗ 📜__init__.py
 ┃ ┃ ┣ 📜alert_banners.py
 ┃ ┃ ┗ 📜__init__.py
 ┃ ┣ 📂bot
 ┃ ┃ ┣ 📂tests
 ┃ ┃ ┣ 📜commands.py
 ┃ ┃ ┗ 📜__init__.py
 ┃ ┣ 📂common
 ┃ ┃ ┣ 📂utils
 ┃ ┃ ┃ ┗ 📜templater.py
 ┃ ┃ ┗ 📜__init__.py
 ┃ ┣ 📂donation
 ┃ ┃ ┣ 📂tests
 ┃ ┃ ┃ ┗ 📜__init__.py
 ┃ ┃ ┗ 📜__init__.py
 ┃ ┣ 📂gemini_llm
 ┃ ┃ ┗ 📂tests
 ┃ ┣ 📂help
 ┃ ┃ ┣ 📂tests
 ┃ ┃ ┃ ┗ 📜__init__.py
 ┃ ┃ ┗ 📜__init__.py
 ┃ ┣ 📂language
 ┃ ┃ ┣ 📂tests
 ┃ ┃ ┃ ┗ 📜__init__.py
 ┃ ┃ ┣ 📂tools
 ┃ ┃ ┃ ┣ 📜alerts_search.py
 ┃ ┃ ┃ ┣ 📜donations_search.py
 ┃ ┃ ┃ ┣ 📜shelthers_search.py
 ┃ ┃ ┃ ┗ 📜tools.py
 ┃ ┃ ┣ 📜llm.py
 ┃ ┃ ┗ 📜__init__.py
 ┃ ┣ 📂location
 ┃ ┃ ┣ 📜location.py
 ┃ ┃ ┗ 📜__init__.py
 ┃ ┣ 📂vision
 ┃ ┃ ┣ 📂tests
 ┃ ┃ ┃ ┣ 📜test_gemini_vision.py
 ┃ ┃ ┃ ┗ 📜__init__.py
 ┃ ┃ ┣ 📜gemini_vision.py
 ┃ ┃ ┗ 📜__init__.py
 ┃ ┗ 📜__init__.py
 ┣ 📂templates
 ┃ ┣ 📜commands.yaml
 ┃ ┗ 📜prompts.yaml
 ┣ 📜app.py
 ┣ 📜poetry.lock
 ┣ 📜pyproject.toml
 ┗ 📜__init__.py
```
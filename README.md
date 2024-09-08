# 🛰️ Polygonize

`Polygonize` é um programa em Python desenvolvido para converter arquivos raster de formato `.tiff` em shapefiles de polígonos. Este programa é especialmente útil para profissionais e pesquisadores que trabalham com dados geoespaciais, permitindo a análise e manipulação avançada de imagens raster.

## Funcionalidades Principais

O `Polygonize` oferece uma série de funcionalidades que tornam o trabalho com dados raster mais eficiente:

1. **Conversão de Raster para Polígonos**:  
   Converte imagens raster (`.tiff`) em arquivos de polígonos (`.shp`), permitindo a análise vetorial de dados geoespaciais. O usuário pode escolher quais bandas e quais cores específicas do raster serão vetorizadas, proporcionando flexibilidade no processo de conversão.

2. **Contagem de Pixels por Valor de Cor**:  
   Conta o número de pixels para cada valor de cor em uma banda específica de um arquivo TIFF. Esta função é útil para entender a distribuição de diferentes valores de pixels (por exemplo, tipos de uso do solo) em uma determinada área geográfica.

3. **Exclusão de Polígonos Baseada em Valores de Pixel**:  
   Permite a exclusão de polígonos específicos durante o processo de conversão com base em um valor de pixel fornecido pelo usuário, facilitando a limpeza e filtragem de dados.

4. **Interface de Linha de Comando Interativa**:  
   O programa utiliza uma interface de linha de comando (CLI) interativa para solicitar ao usuário as informações necessárias para o processamento, como o número da banda e as cores desejadas.

5. **Barra de Progresso para Feedback ao Usuário**:  
   Utiliza a biblioteca `tqdm` para exibir uma barra de progresso que mostra o andamento do processo de conversão, proporcionando uma melhor experiência ao usuário.

## Aplicações

`Polygonize` pode ser utilizado em diversas áreas, incluindo:

- **Análise de Uso do Solo e Cobertura Vegetal**:  
  Convertendo dados raster de uso do solo em polígonos vetoriais, permitindo análise espacial precisa de diferentes tipos de cobertura do solo, como floresta, água, áreas urbanas, etc.

- **Monitoramento Ambiental**:  
  Com dados de satélite, pode-se monitorar mudanças ambientais, como desmatamento, expansão urbana, e variações no nível da água.

- **Geoprocessamento em Agricultura**:  
  Análise de imagens de satélite para determinar tipos de culturas, saúde das plantas, e padrões de irrigação, ajudando no planejamento agrícola.

- **Gestão de Recursos Naturais**:  
  Para a gestão de recursos como florestas, bacias hidrográficas, e parques naturais, convertendo dados raster em polígonos vetoriais para uma análise mais detalhada.

## Requisitos Técnicos

Para utilizar o `Polygonize`, são necessárias algumas dependências, incluindo bibliotecas específicas para manipulação de dados raster e vetoriais. Abaixo estão os requisitos necessários para instalar e executar o programa:

- Python 3.x
- [GDAL (Geospatial Data Abstraction Library)](https://gdal.org/)
- `opencv-python`
- `rasterio`
- `numpy`
- `osgeo` (parte do GDAL)
- `tqdm`
- `fluss-tools`

Você pode instalar as dependências usando o comando:

```bash
pip install opencv-python rasterio numpy gdal tqdm flusstools
```

## Como Funciona?

### Passo a Passo para Usar o Polygonize

1. **Configure o Caminho do Arquivo TIFF**:
   No script Python, defina o caminho para o arquivo TIFF que você deseja processar, atribuindo-o à variável `IMAGE_PATH`.

2. **Execute o Script**:
   Execute o script Python na linha de comando:
   ```bash
   python polygonize.py
   ```

3. **Selecione a Banda e Cor para Processamento**:
   O programa solicitará que você escolha a banda da imagem TIFF que deseja processar. Em seguida, você poderá escolher se deseja vetorizar todas as cores ou apenas uma cor específica.

4. **Visualize o Progresso da Conversão**:
   A conversão de raster para polígonos será exibida com uma barra de progresso interativa. 

5. **Verifique o Resultado**:
   Os shapefiles gerados serão salvos em uma pasta de saída especificada. Eles podem ser carregados em software de SIG, como QGIS ou ArcGIS, para análise posterior.

## Contribuições

Se você tiver ideias para melhorias ou encontrar um bug, sinta-se à vontade para abrir uma _issue_ ou enviar um _pull request_.

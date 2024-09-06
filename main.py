import cv2
import rasterio
from rasterio.transform import from_origin
import numpy as np
from osgeo import gdal, ogr
import os
from flusstools.geotools import *
from tqdm import tqdm
from random import randint

gdal.PushErrorHandler('CPLQuietErrorHandler')
RANDOM_VALUE = randint(0, 100)

def polygonize_callback(complete, message, callback_data):
    """
    Callback da barra de loading.
    :param complete: Porcentagem completa.
    :param message: Mensagem.
    :param callback_data: Dados de retorno.
    """
    pbar.update(int(complete * 100) - pbar.n)

def count_pixels_by_band(file_path, band_num):
    """
    Conta o número de pixels para cada valor de cor em uma banda específica de um arquivo TIFF.
    :param file_path: Caminho para o arquivo TIFF.
    :param band_num: Número da banda para contar os pixels.
    :return: Um dicionário com a contagem de pixels para cada valor de cor.
    """

    x = gdal.Open(file_path)

    if x is None:
        print("Não foi possível abrir o arquivo TIFF.")
        return

    # Verificar se o número da banda é válido
    if band_num < 1 or band_num > x.RasterCount:
        print("Número de banda inválido.")
        return

    # Obter a banda selecionada
    band = x.GetRasterBand(band_num)
    data = band.ReadAsArray()

    # Calcular a contagem de pixels para cada valor de cor
    unique_colors, counts = np.unique(data, return_counts=True)

    # Criar um dicionário para armazenar a contagem de cada valor de cor
    color_counts = {color: count for color, count in zip(unique_colors, counts)}
    if len(color_counts) > 2:
        colors_response = input(f'O arquivo possui {len(color_counts)} cor(es) na banda {band_num}. Deseja continuar o processamento? (S para Sim, N para Não): ').upper()

        if colors_response == "S":
            raster2polygon(IMAGE_PATH, tar_shp, band_number=band_num)
        elif colors_response == "N":
            print('Obrigado.')
            exit(0)
    else:
        color_list = []
        # Imprimir a contagem de pixels para cada valor de cor
        for color, count in color_counts.items():
            #print(f"Cor {int(color)} na banda {band_num}: {int(count)} pixels")
            color_ = str(color)
            print(f"Cor {color_.split('.')[0]} na banda {band_num}: {int(count)} pixels")

            color_list.append(color_)

    # Fechar o dataset
    x = None
    return color_list


# Função para converter um raster em um shapefile de polí­gonos
def raster2polygon(file_name, out_shp_fn, band_number=2, field_name="values", pixel_value_to_delete=None):
    """
    Converte um raster em um shapefile de polí­gonos, excluindo polí­gonos com um valor de pixel especí­fico
    :param file_name: Nome do arquivo raster de destino, incluindo o diretório; deve terminar com ".tif"
    :param out_shp_fn: Nome do shapefile de destino (com diretório, por exemplo, "C:/temp/poly.shp")
    :param band_number: Número da banda raster a ser aberta (padrão: 1)
    :param field_name: Nome do campo onde os valores dos pixels do raster serão armazenados (padrão: "values")
    :param pixel_value_to_delete: Valor do pixel a ser excluí­do dos polí­gonos resultantes (padrão: None)
    :return: Nenhum
    """
    try:
        # Abra o raster de entrada
        raster, raster_band = open_raster(file_name, band_number=band_number)


        # Crie um novo shapefile usando a função "create_shp"
        new_shp = create_shp(out_shp_fn, layer_name="raster_data", layer_type="polygon")
        dst_layer = new_shp.GetLayer()

        # Crie um novo campo para armazenar os valores
        new_field = ogr.FieldDefn(field_name, ogr.OFTInteger)
        dst_layer.CreateField(new_field)

        global pbar
        with tqdm(total=100, desc="Convertendo raster para polígonos...") as pbar:
            # Converta o raster em polígonos (Polygonize)
            gdal.Polygonize(raster_band, None, dst_layer, 0, [], callback=polygonize_callback)

        # Se um valor de pixel especí­fico for fornecido, exclua os polí­gonos correspondentes
        if pixel_value_to_delete is not None:
            dst_layer.ResetReading()  # Reinicie a leitura para percorrer todos os polí­gonos
            for feature in dst_layer:
                if feature.GetField(field_name) == pixel_value_to_delete:
                    dst_layer.DeleteFeature(feature.GetFID())

        # Crie um arquivo de projeção
        srs = get_srs(raster)
        make_prj(out_shp_fn, int(srs.GetAuthorityCode(None)))

        print("Sucesso: Arquivo gerado - %s" % str(out_shp_fn))
    except Exception as error:
        print(f"Ocorreu um erro inesperado. Detalhe do erro: {error}")

def get_band_numbers(file_path):
    """
    Obtém os números de todas as bandas de um arquivo TIFF.
    :param file_path: Caminho para o arquivo TIFF.
    """
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f'Arquivo .tif não encontrado: {file_path}')
        # Abrir o arquivo TIFF para obter o número de bandas
        data_file = gdal.Open(file_path)

        if data_file is None:
            raise ValueError(f'Erro ao ler imagem: {data_file}.')
        else:
            # Obter o número de bandas
            num_bands = data_file.RasterCount

            if num_bands > 0:
                print(f"O arquivo tem {num_bands} banda(s).")

                while True:
                    # Solicitar ao usuário o número da banda desejada
                    band_number = int(input(f"Digite o número da banda (1 a {num_bands}): "))

                    if band_number not in range(1, num_bands + 1):
                        print('Número de banda inválido. Digite um número existente.')
                    else:
                        # Chamar a função para contar os pixels para a banda especificada
                        color_list = count_pixels_by_band(IMAGE_PATH, band_number)

                        if isinstance(color_list, list) and color_list:
                            # Perguntar se o usuário quer vetorizar todas as cores
                            vectorize_all_colors = input("Deseja vetorizar todas as cores? (S para Sim, N para Não): ").upper()

                            if vectorize_all_colors == "S":
                                pixel_value_to_delete = None
                                break
                            elif vectorize_all_colors == "N":
                                # Solicitar ao usuário o número da cor que deseja vetorizar
                                color_to_vectorize = int(input("Digite o número da cor que deseja vetorizar: "))
                                if color_to_vectorize not in range(len(color_list)):
                                    print('Cor não existente. Por favor, digite um valor válido.')
                                else:
                                    # Inverter os valores do índice na lista color_list
                                    pixel_value_to_delete = 1 if color_to_vectorize == 0 else 0
                                    break
                            else:
                                print('Operação inválida. Tente novamente.')
                        else:
                            print('Erro ao obter a lista de cores.')
                # Chamar a função raster2polygon com o valor do pixel a ser excluído
                raster2polygon(IMAGE_PATH, tar_shp, band_number=band_number, pixel_value_to_delete=pixel_value_to_delete)
            else:
                print("O arquivo não possui bandas.")
    except FileNotFoundError as e:
        print('Arquivo .tif não encontrado.')
    except Exception as e:
        print('Houve um erro inesperado ao executar o arquivo. Detalhe do erro: ', e)

# Caminho para o arquivo TIFF
IMAGE_PATH = r"" # Aqui vai um arquivo em formato GeoTIFF(.tiff)

# Obtendo o diretório do arquivo TIFF
image_directory = os.path.dirname(IMAGE_PATH)

# Inicializando um contador para incrementar o número da pasta
folder_counter = 1

# Enquanto a pasta existir, incremente o contador
while True:
    # Criando o nome da pasta de saída
    output_folder_name = f"output_folder_{folder_counter}"

    # Obtendo o caminho completo para a pasta de saída
    output_folder_path = os.path.join(image_directory, output_folder_name)

    # Verificando se a pasta já existe
    if not os.path.exists(output_folder_path):
        # Se não existir, criamos a pasta e saímos do loop
        os.makedirs(output_folder_path)
        break
    else:
        # Se existir, incrementamos o contador e continuamos o loop
        folder_counter += 1

# Caminho para o shapefile de destino dentro da pasta de saída
tar_shp = os.path.join(output_folder_path, "teste_6.shp")

# Chame a função get_band_numbers
get_band_numbers(IMAGE_PATH)
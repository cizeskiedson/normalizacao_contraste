import numpy as np
import matplotlib.pyplot as plt
import os
import cv2
import sys
import getopt
from skimage.filters.rank import maximum, minimum

def help():
    print("\nErro na leitura dos parametros\n")
    print("Digite python3 trab.py -i nome_da_imagem -m tamanho da mascara\n")
    print("\nImagens disponiveis: \n")
    print(os.listdir(dirImagens()))
    print("================================\n")

def dirImagens():
    dir_atual = os.path.dirname(os.path.realpath('__file__'))
    return os.path.join(dir_atual, 'fotos/')

def leArquivo():
    """Funcao que le os parametros e a foto.
    """
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'i:m:h', ['imagem=', 'mascara=', 'help'])
    except getopt.GetoptError:
        help()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            help()
            sys.exit(2)
        elif opt in ('-i', '--imagem'):
            imagem = arg
        elif opt in ('-m', '--paleta'):
            tamMascara = int(arg)
        else:
            sys.exit(2)
    nome_img = os.path.join(dirImagens(), imagem)
    img = cv2.imread(nome_img, cv2.IMREAD_GRAYSCALE)
    return img, tamMascara

def criaMascara(tamMascara):
    """ Cria mascara
    """
    return np.ones((tamMascara,tamMascara))


def normalizacao(img, mascara):
    """Aplica normalizacao local de contraste
    """
    max = maximum(img, mascara)
    min = minimum(img, mascara)
    print(max)
    print(min)
    p1 = np.subtract(img, min)
    p2 = np.subtract(max, min)
    np.place(p2, p2 == 0, 0.0000001) 
    with np.errstate(invalid='ignore', divide='ignore'):
        p3 = np.true_divide(p1, p2) 
    return p3 * 255


def main():
    """Fluxo principal.
    """
    img, tamMascara = leArquivo()
    mascara =  criaMascara(tamMascara)
    resultado = normalizacao(img, mascara)
    cv2.imshow('image', resultado)
    cv2.waitKey(0)



if __name__ == "__main__":
    main()
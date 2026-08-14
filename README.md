# Air Canvas - Aplicativo de Desenho por Visão Computacional

## Visão Geral
O Air Canvas é uma aplicação interativa desenvolvida em Python que utiliza visão computacional para permitir o desenho em tempo real através de gestos manuais. O sistema processa o feed de vídeo da webcam, utilizando as bibliotecas OpenCV para o processamento de imagens e MediaPipe para a detecção e o rastreamento preciso de pontos de referência das mãos.

## Funcionalidades
- Rastreamento espacial de mãos e dedos em tempo real.
- Modo de desenho ativado pela extensão exclusiva do dedo indicador.
- Modo de navegação e seleção ativado pela extensão simultânea dos dedos indicador e médio.
- Interface de seleção no topo da tela contendo as opções de cores (Azul, Verde e Vermelho) e a funcionalidade de limpeza da área de trabalho.
- Renderização de matrizes e vetores gráficos sobrepostos ao fluxo contínuo de vídeo.

## Pré-requisitos
- Ambiente com Python 3.11 configurado no `PATH`.
- Webcam integrada ou externa funcional.
- Gerenciador de pacotes `pip` atualizado.

## Instalação

1. Clone este repositório para o seu ambiente local:
   ```bash
   git clone [https://github.com/SEU_USUARIO/NOME_DO_REPOSITORIO.git](https://github.com/SEU_USUARIO/NOME_DO_REPOSITORIO.git)

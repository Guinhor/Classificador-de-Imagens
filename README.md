# Classificador de Imagens CIFAR-10 com Flask API e Web Interface

Este projeto implementa um classificador de imagens baseado em uma Rede Neural Convolucional (CNN) para o dataset CIFAR-10. Ele é exposto como uma API RESTful utilizando Flask e possui uma interface web simples para upload de imagens e visualização das predições, além de um mecanismo de coleta de feedback para aprendizado ativo.

## Funcionalidades

- **Classificação de Imagens:** Prediz a classe de uma imagem (10 categorias do CIFAR-10: avião, automóvel, pássaro, gato, veado, cachorro, sapo, cavalo, navio, caminhão).
- **API RESTful:** Backend em Flask para receber imagens e retornar predições em formato JSON.
- **Interface Web:** Uma página HTML/JavaScript para upload visual de imagens e exibição dos resultados.
- **Coleta de Feedback:** Botões "Correto/Incorreto" na interface web para que o usuário possa fornecer feedback sobre a predição. Este feedback, juntamente com a imagem, é armazenado para futuro retreinamento do modelo (Aprendizado Ativo).

## Pré-requisitos

Para executar este projeto, você precisará ter o seguinte software instalado em seu sistema:

-   **Python 3.10.x** (Versão recomendada para compatibilidade com TensorFlow 2.15.0)
-   **Miniconda** (Recomendado para gerenciamento de ambientes Python e dependências)
-   **Git** (Para clonar este repositório)
-   **Visual Studio Code** (IDE recomendada para desenvolvimento)

## Instalação e Configuração

Siga os passos abaixo para configurar e executar o projeto em seu ambiente local.

### 1. Clonar o Repositório

Abra o terminal (Anaconda Prompt ou terminal integrado do VS Code) e execute o comando:

git clone [https://github.com/Guinhor/Classificador-de-Imagens.git](https://github.com/Guinhor/Classificador-de-Imagens.git)
cd Classificador-de-Imagens

### 2. Criar e Ativar o Ambiente Conda
É altamente recomendado usar um ambiente Conda para isolar as dependências do projeto.

# Criar o ambiente com Python 3.10
conda create --name cifar_env python=3.10

# Ativar o ambiente
conda activate cifar_env

### 3. Instalar as Dependências
Com o ambiente cifar_env ativado, instale todas as bibliotecas necessárias:

pip install Flask tensorflow==2.15.0 numpy opencv-python Pillow keras==2.15.0

### 4. Execução da API
Com todos os pré-requisitos instalados e o ambiente Conda ativado no terminal do VS Code, você pode iniciar a API:

Certifique-se de que está na pasta raiz do projeto (Classificador-de-Imagens) no terminal.

Execute o script da API:

python app.py

O terminal exibirá mensagens do Flask, incluindo:

* Running on [http://0.0.0.0:5000](http://0.0.0.0:5000)
* Running on [http://127.0.0.1:5000](http://127.0.0.1:5000)
Sua API agora está ativa e acessível.

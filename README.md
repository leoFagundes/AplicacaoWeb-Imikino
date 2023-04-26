# Aplicação web Imikino
## Site de avaliação de jogos

Esta é uma aplicação web feita em Flask chamada Imikino, é um site de avaliação de jogos com sistema de login.
Foi um projeto bem interessante e aprendi muito na execução dele.

### Bibliotecas que foram usadas:

* pip install Flask -> Framework de python para criação de sites
* pip install flask-wtf -> Para criação de formulários com FlaskForm
* pip install email_validator -> Para validar e-mails no falsk-wtf
* pip install sqlalchemy -> É o banco de dados
* pip install flask-sqlalchemy
* pip install flask-bcrypt -> Para criptografar a senha
* pip install flask-login -> Para fazer o sistema de login do site
* pip install Pillow -> Para reduzir o tamanho da imagem ao editar o perfil
* pip install gunicorn -> Para colocar o site no ar com o heroku
* pip install requests -> Para uso da API da steam
* pip install pandas -> Para uso da API da steam

## Instruções para acesso:
- Após clonar esse repositório instale todas as bibliotecas mencionadas acima e rode o arquivo main.py. Em seguida entre no link que ele forneceu no seu terminal.

## Demonstração do site:

### <p align='center'>PÁGINA INICIAL</p>

![Imagem](https://github.com/leoFagundes/AplicacaoWeb-Imikino/blob/main/imikino/static/images/imgREADME/1-home.png)
<br>
![Imagem](https://github.com/leoFagundes/AplicacaoWeb-Imikino/blob/main/imikino/static/images/imgREADME/2-home.png?raw=true)

<hr>

### <p align='center'>PÁGINA SOBRE</p>

![Imagem](https://github.com/leoFagundes/AplicacaoWeb-Imikino/blob/main/imikino/static/images/imgREADME/3-sobre.png?raw=true)

<hr>

### <p align='center'>PÁGINA CADASTRO/LOGIN</p>

![Imagem](https://github.com/leoFagundes/AplicacaoWeb-Imikino/blob/main/imikino/static/images/imgREADME/4-cadastro.png?raw=true)
<br>
![Imagem](https://github.com/leoFagundes/AplicacaoWeb-Imikino/blob/main/imikino/static/images/imgREADME/5-login.png?raw=true)

<hr>

### <p align='center'>PÁGINA HOME APÓS LOGAR</p>

![Imagem](https://github.com/leoFagundes/AplicacaoWeb-Imikino/blob/main/imikino/static/images/imgREADME/6-homeLogado.png?raw=true)

<hr>

### <p align='center'>PÁGINA USUÁRIOS</p>
<p align='center'><i>Mostra todos os usuários cadastrados do site</i></p>

![Imagem](https://github.com/leoFagundes/AplicacaoWeb-Imikino/blob/main/imikino/static/images/imgREADME/7-usuarios.png?raw=true)

<hr>

### <p align='center'>PÁGINA JOGOS</p>
<p align='center'><i>Mostra todos os jogos cadastrados no site e é possível avaliar cada um.</i></p>
<p align='center'><i>A avaliação de cada jogo é uma média da avaliação de todos os usuários</i></p>

![Imagem](https://github.com/leoFagundes/AplicacaoWeb-Imikino/blob/main/imikino/static/images/imgREADME/8-pageJogos.png?raw=true)


<hr>

### <p align='center'>PÁGINA PERFIL/EDITAR PERFIL</p>

![Imagem](https://github.com/leoFagundes/AplicacaoWeb-Imikino/blob/main/imikino/static/images/imgREADME/9-meuPerfil.png?raw=true)
<br>
![Imagem](https://github.com/leoFagundes/AplicacaoWeb-Imikino/blob/main/imikino/static/images/imgREADME/10-editarPerfil.png?raw=true)

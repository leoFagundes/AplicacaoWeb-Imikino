import requests
from flask import render_template, flash, redirect, url_for, request, jsonify, make_response
from imikino import app, database, bcrypt
from imikino.forms import FormLogin, FormCriarConta, FormEditarPerfil, Avaliacoes, IdSteam
from imikino.models import Usuario, Jogos, Avaliacao
from flask_login import login_user, logout_user, current_user, login_required
import secrets
import os
from PIL import Image #vamos usar para reduzir o tamanho da imagem
from sqlalchemy.sql import func
import pandas as pd
import json


# Exemplo de requisição usando SteamAPI


def steam(id):
    response = requests.get("http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/"
                            f"?key=F5EAABA4A3A664FE469560765E3839E4&steamid={id}&format=json&include_appinfo=true").text
    response_info = json.loads(response)
    game_list = []
    for game_info in response_info['response']['games']:
        game_list.append([game_info['appid'], game_info['name'], game_info['playtime_forever']])
    games_df = pd.DataFrame(data=game_list, columns=['appid', 'name', 'playtime_forever'])
    lista_jogo_horas = []
    for value in games_df.get("name"):
        lista_jogo_horas.append([value])
    for i, value in enumerate(games_df.get("playtime_forever")):
        lista_jogo_horas[i].append(value)
    return lista_jogo_horas
    return jsonify(response)


# @app.route('/steamImage')
# def steamImage():
#     response = requests.get("http://media.steampowered.com/steamcommunity/public/images/apps/108600/2bd4642ae337e378e7b04a19d19683425c5f81a4.jpg")
#
#     return response.request


@app.route('/', methods=['GET', 'POST'])
def home():
    form = IdSteam()

    if current_user.is_authenticated:
        if form.validate_on_submit():
            id = form.id_steam.data
            
            try:
                lista_jogo_horas = steam(id)

                lista_jogo_horas = sorted(lista_jogo_horas, key = lambda x: x[1], reverse = True)

                for lista in lista_jogo_horas:
                    lista[1] = int(lista[1]/60)

                if len(lista_jogo_horas) > 3:
                    lista_jogo_horas = lista_jogo_horas[0:3]
                return redirect(f'/{id}') 

            except:
                return redirect(f'/error') 


        jogos = Jogos.query.all()
        lista_melhor_avaliado = []
        for jogo in jogos:
            lista_melhor_avaliado.append([jogo.nome, jogo.media_jogos])
        lista_melhor_avaliado = sorted(lista_melhor_avaliado, key=lambda l:l[1], reverse=True)
        lista_melhor_avaliado = lista_melhor_avaliado[0:5]

        usuarios = Usuario.query.all()
        lista_favoritos = []
        for usuario in usuarios:
            if 'Não Informado' in usuario.jogo_favorito:
                pass
            else:
                lista_favoritos.append(usuario.jogo_favorito)

        #id, nome, ocorrencia favorito
        lista_lista_favorito = []
        for jogo in jogos:
            if lista_favoritos.count(jogo.nome) > 0:
                lista_lista_favorito.append([jogo.nome, lista_favoritos.count(jogo.nome)])

        lista_lista_favorito = sorted(lista_lista_favorito, key = lambda x: x[1])
        lista_lista_favorito = lista_lista_favorito[::-1]
        lista_lista_favorito = lista_lista_favorito[:5]
        
        foto_perfil = url_for('static', filename='foto_perfil/{}'.format(current_user.foto_perfil))
        return render_template('home.html', foto_perfil=foto_perfil, lista_melhor_avaliado=lista_melhor_avaliado, lista_lista_favorito=lista_lista_favorito, form=form)

    jogos = Jogos.query.all()
    lista_melhor_avaliado = []
    for jogo in jogos:
        lista_melhor_avaliado.append([jogo.nome, jogo.media_jogos])
    lista_melhor_avaliado = sorted(lista_melhor_avaliado, key=lambda l:l[1], reverse=True)
    lista_melhor_avaliado = lista_melhor_avaliado[0:5]

    usuarios = Usuario.query.all()
    lista_favoritos = []
    for usuario in usuarios:
        if 'Não Informado' in usuario.jogo_favorito:
            pass
        else:
            lista_favoritos.append(usuario.jogo_favorito)

    #id, nome, ocorrencia favorito
    lista_lista_favorito = []
    for jogo in jogos:
        if lista_favoritos.count(jogo.nome) > 0:
            lista_lista_favorito.append([jogo.nome, lista_favoritos.count(jogo.nome)])

    lista_lista_favorito = sorted(lista_lista_favorito, key = lambda x: x[1])
    lista_lista_favorito = lista_lista_favorito[::-1]
    lista_lista_favorito = lista_lista_favorito[:5]
    return render_template('home.html', lista_melhor_avaliado=lista_melhor_avaliado, lista_lista_favorito=lista_lista_favorito)



@app.route('/<id>')
@login_required #precisa estar logado para acessar essa página
def home_id(id):
    form = IdSteam()

    if current_user.is_authenticated:
        if id == 'error':
            jogos = Jogos.query.all()
            lista_melhor_avaliado = []
            for jogo in jogos:
                lista_melhor_avaliado.append([jogo.nome, jogo.media_jogos])
            lista_melhor_avaliado = sorted(lista_melhor_avaliado, key=lambda l:l[1], reverse=True)
            lista_melhor_avaliado = lista_melhor_avaliado[0:5]

            usuarios = Usuario.query.all()
            lista_favoritos = []
            for usuario in usuarios:
                if 'Não Informado' in usuario.jogo_favorito:
                    pass
                else:
                    lista_favoritos.append(usuario.jogo_favorito)

            #id, nome, ocorrencia favorito
            lista_lista_favorito = []
            for jogo in jogos:
                if lista_favoritos.count(jogo.nome) > 0:
                    lista_lista_favorito.append([jogo.nome, lista_favoritos.count(jogo.nome)])

            lista_lista_favorito = sorted(lista_lista_favorito, key = lambda x: x[1])
            lista_lista_favorito = lista_lista_favorito[::-1]
            lista_lista_favorito = lista_lista_favorito[:5]
            foto_perfil = url_for('static', filename='foto_perfil/{}'.format(current_user.foto_perfil))
            return render_template('home.html', foto_perfil=foto_perfil, lista_melhor_avaliado=lista_melhor_avaliado, lista_lista_favorito=lista_lista_favorito, form=form)

        lista_jogo_horas = steam(id)
        lista_jogo_horas = sorted(lista_jogo_horas, key = lambda x: x[1], reverse = True)

        for lista in lista_jogo_horas:
            lista[1] = int(lista[1]/60)

        if len(lista_jogo_horas) > 3:
            lista_jogo_horas = lista_jogo_horas[0:3]

        jogos = Jogos.query.all()
        lista_melhor_avaliado = []
        for jogo in jogos:
            lista_melhor_avaliado.append([jogo.nome, jogo.media_jogos])
        lista_melhor_avaliado = sorted(lista_melhor_avaliado, key=lambda l:l[1], reverse=True)
        lista_melhor_avaliado = lista_melhor_avaliado[0:5]

        usuarios = Usuario.query.all()
        lista_favoritos = []
        for usuario in usuarios:
            if 'Não Informado' in usuario.jogo_favorito:
                pass
            else:
                lista_favoritos.append(usuario.jogo_favorito)

        #id, nome, ocorrencia favorito
        lista_lista_favorito = []
        for jogo in jogos:
            if lista_favoritos.count(jogo.nome) > 0:
                lista_lista_favorito.append([jogo.nome, lista_favoritos.count(jogo.nome)])

        lista_lista_favorito = sorted(lista_lista_favorito, key = lambda x: x[1])
        lista_lista_favorito = lista_lista_favorito[::-1]
        lista_lista_favorito = lista_lista_favorito[:5]
        
        foto_perfil = url_for('static', filename='foto_perfil/{}'.format(current_user.foto_perfil))
        return render_template('home.html', foto_perfil=foto_perfil, lista_melhor_avaliado=lista_melhor_avaliado, lista_lista_favorito=lista_lista_favorito, form=form, lista_jogo_horas=lista_jogo_horas)

    jogos = Jogos.query.all()
    lista_melhor_avaliado = []
    for jogo in jogos:
        lista_melhor_avaliado.append([jogo.nome, jogo.media_jogos])
    lista_melhor_avaliado = sorted(lista_melhor_avaliado, key=lambda l:l[1], reverse=True)
    lista_melhor_avaliado = lista_melhor_avaliado[0:5]

    usuarios = Usuario.query.all()
    lista_favoritos = []
    for usuario in usuarios:
        if 'Não Informado' in usuario.jogo_favorito:
            pass
        else:
            lista_favoritos.append(usuario.jogo_favorito)

    #id, nome, ocorrencia favorito
    lista_lista_favorito = []
    for jogo in jogos:
        if lista_favoritos.count(jogo.nome) > 0:
            lista_lista_favorito.append([jogo.nome, lista_favoritos.count(jogo.nome)])

    lista_lista_favorito = sorted(lista_lista_favorito, key = lambda x: x[1])
    lista_lista_favorito = lista_lista_favorito[::-1]
    lista_lista_favorito = lista_lista_favorito[:5]
    return render_template('home.html', lista_melhor_avaliado=lista_melhor_avaliado, lista_lista_favorito=lista_lista_favorito)



@app.route('/sobre')
def sobre():
    if current_user.is_authenticated:
        foto_perfil = url_for('static', filename='foto_perfil/{}'.format(current_user.foto_perfil))
        return render_template('sobre.html', foto_perfil=foto_perfil)
    return render_template('sobre.html')


@app.route('/usuarios')
@login_required #precisa estar logado para acessar essa página
def usuarios():
    lista_usuarios  = Usuario.query.all()

    if current_user.is_authenticated:
        foto_perfil = url_for('static', filename='foto_perfil/{}'.format(current_user.foto_perfil))
        return render_template('usuarios.html', foto_perfil=foto_perfil, lista_usuarios=lista_usuarios)
    return render_template('usuarios.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form_login = FormLogin()

    if form_login.validate_on_submit():
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()
        # verificar se o usuario e a senha estão corretas
        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
            # fazer o login
            login_user(usuario, remember=form_login.lembrar_dados.data)
            # fez login com sucesso
            # exibir mensagem de sucesso -> flash
            flash(f'Login feito com sucesso para o e-mail {form_login.email.data}', 'alert-primary')  # .data serve para pegar o que a pessoa escreveu no campo de texto
              
            #verificar se existie o parâmetro next (caso ele tenha tentado acessar uma página que só é permitida estando logado então ele ganha o parâmetro next=página que ele tentou acessar e ao fazer login ele em vez de ir para a home ele vai para o next)
            par_next = request.args.get('next') #pegando o valor do parâmetro next e colocando em uma variável
            if par_next:
                return redirect(par_next)
            # redirecionar para a home page -> redirect
            else:
                return redirect(url_for('home'))
        else:
            flash(f'Falha no Login. E-mail ou Senha Incorretos', 'alert-danger')
    return render_template('login.html', form_login=form_login)


@app.route('/criar-conta', methods=['GET', 'POST'])
def criarConta():
    form_criarconta = FormCriarConta()

    if form_criarconta.validate_on_submit():
        # criptografar a senha
        senha_cript = bcrypt.generate_password_hash(form_criarconta.senha.data)
        # criar o Usuario
        usuario = Usuario(username=form_criarconta.username.data, email=form_criarconta.email.data, senha=senha_cript)
        # adicionar a sessão
        database.session.add(usuario)
        # commitar a sessão
        database.session.commit()
        # -----------------------
        # fez login com sucesso
        # exibir mensagem de sucesso -> flash
        flash(f'Bem-vindo(a) ao time, {form_criarconta.username.data}!! Conta criada com sucesso', 'alert-primary')  # .data serve para pegar o que a pessoa escreveu no campo de texto
        # redirecionar para a home page -> redirect
        return redirect(url_for('login'))
    return render_template('criarConta.html', form_criarconta=form_criarconta)


@app.route('/sair')
@login_required #precisa estar logado para acessar essa página
def sair():
    logout_user()
    flash(f'Logout feito com sucesso. Até logo!', 'alert-primary')
    return redirect(url_for('home'))


@app.route('/perfil')
@login_required #precisa estar logado para acessar essa página
def perfil():
    lista_avaliacoes = Avaliacao.query.filter_by(id_usuario=current_user.id).all()
    qntde_avaliacao = len(lista_avaliacoes)
    if current_user.is_authenticated:
        foto_perfil = url_for('static', filename='foto_perfil/{}'.format(current_user.foto_perfil))
        return render_template('perfil.html', foto_perfil=foto_perfil, qntde_avaliacao=qntde_avaliacao)


def salvar_imagem(imagem):
    #adicionar um código aleatório no nome da imagem para evitar que duas imagens tenham o mesmo nome
    codigo = secrets.token_hex(6)
    nome, extensao = os.path.splitext(imagem.filename)
    nome_arquivo = nome + codigo + extensao

    caminho_completo = os.path.join(app.root_path, 'static/foto_perfil', nome_arquivo) #caminho da pasta imikino

    #reduzir o tamanho da imagem
    tamanho = (400, 400)
    imagem_reduzida = Image.open(imagem)
    imagem_reduzida.thumbnail(tamanho)

    #salvar a imagem na pasta fotos_perfil
    imagem_reduzida.save(caminho_completo)
    return nome_arquivo


@app.route('/perfil/editar', methods=['GET', 'POST'])
@login_required #precisa estar logado para acessar essa página
def editar_perfil():
    form = FormEditarPerfil()

    lista_avaliacoes = Avaliacao.query.filter_by(id_usuario=current_user.id).all()
    qntde_avaliacao = len(lista_avaliacoes)

    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.jogo_favorito = form.jogo_favorito.data
        if form.foto_perfil.data:
            #mudar o campo foto_perfil do usuario para o novo nome da imagem
            nome_imagem = salvar_imagem(form.foto_perfil.data)
            current_user.foto_perfil = nome_imagem
        database.session.commit()
        flash(f'Perfil atualizado com Sucesso', 'alert-primary')
        return redirect(url_for('perfil'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.jogo_favorito.data = current_user.jogo_favorito

    if current_user.is_authenticated:
        foto_perfil = url_for('static', filename='foto_perfil/{}'.format(current_user.foto_perfil))
        return render_template('editarperfil.html', foto_perfil=foto_perfil, form=form, qntde_avaliacao=qntde_avaliacao)


@app.route('/jogos')
@login_required #precisa estar logado para acessar essa página
def jogos():
    '''
    #Apenas para criar os jogos no banco de dados
    jogo1 = Jogos(id= 1, nome='Cuphead', lancamento='2017', descricao='Cuphead é um jogo eletrônico de run and gun e plataforma criado pelos irmãos canadenses Chad e Jared Moldenhauer através da Studio MDHR', genero='Shoot em up, Run and gun', desenvolvedor='MDHR', foto_jogo='cuphead.jpg')
    jogo2 = Jogos(id= 2, nome='Diablo III', lancamento='2012', descricao='Diablo III é um RPG de ação hack and slash desenvolvido pela Blizzard Entertainment, o terceiro título da série Diablo', genero='RPG, Hack and slash', desenvolvedor='Blizzard', foto_jogo='diablo.jpg')
    jogo3 = Jogos(id= 3, nome='Fortnite', lancamento='2017', descricao='Fortnite é um jogo eletrônico multijogador online, desenvolvido pela Epic Games e lançado como diferentes modos de jogo que compartilham a mesma jogabilidade e motor gráfico de jogo', genero='battle royale, multijogador', desenvolvedor='Epic Games', foto_jogo='fortnite.jpg')
    jogo4 = Jogos(id= 4, nome='League of Legends', lancamento='2009', descricao='League of Legends é um jogo eletrônico do gênero multiplayer online battle arena desenvolvido e publicado pela Riot Games', genero='MOBA, multijogador', desenvolvedor='Riot Games', foto_jogo='lol.jpg')
    jogo5 = Jogos(id= 5, nome='Overwatch', lancamento='2016', descricao='Overwatch é um jogo eletrônico multijogador de tiro em primeira pessoa desenvolvido e publicado pela Blizzard Entertainment', genero='FPS, multijogador', desenvolvedor='Blizzard', foto_jogo='ow.jpg')
    jogo6 = Jogos(id= 6, nome='Stardew Valley', lancamento='2016', descricao='Stardew Valley é um jogo de videogame, dos gêneros RPG e simulação, desenvolvido por Eric Barone e publicado pela ConcernedApe e pela Chucklefish', genero='simulação, RPG', desenvolvedor='ConcernedApe', foto_jogo='stardewvalley.jpg')
    jogo7 = Jogos(id= 7, nome='Counter-Strike: GO', lancamento='2012', descricao='Counter-Strike é uma série de jogos eletrônicos de tiro em primeira pessoa multiplayer, no qual times de terroristas e contra-terroristas batalham entre si', genero='Tiro tático, multiplayer', desenvolvedor='Valve Corporation', foto_jogo='cs_go.png')
    jogo8 = Jogos(id= 8, nome='World of Warcraft', lancamento='2004', descricao='WOW é um jogo onde você cria e vive com seus personagens em um mundo virtual junto com milhões de outras pessoas. Você pode escolher entre várias raças como humano, elfo, goblin ou até um panda', genero='MMORPG, Fantasia', desenvolvedor='Blizzard Entertainment ', foto_jogo='wow.jpg')
    jogo9 = Jogos(id= 9, nome='The Witcher 3', lancamento='2015', descricao='The Witcher 3 conta a aventura do bruxo Geralt de Rívia em busca da sua filha, Ciri, enquanto enfrenta inimigos mortais e explora um mundo cheio de possibilidades, desafios e aventuras', genero='Mundo aberto, RPG', desenvolvedor='CD Projekt RED', foto_jogo='the witcher.jpg')
    jogo10 = Jogos(id= 10, nome='Minecraft', lancamento='2011', descricao='Minecraft é um jogo eletrônico sandbox de sobrevivência criado pelo desenvolvedor sueco Markus "Notch" Persson e posteriormente desenvolvido e publicado pela Mojang Studios', genero='Sandbox, Sobrevivência', desenvolvedor='Mojang Studios', foto_jogo='minecraft.png')
    jogo11 = Jogos(id= 11, nome='Cities: Skylines', lancamento='2015', descricao='Cities: Skylines é um jogo de construção de cidade singleplayer produzido pela Colossal Order e publicado pela Paradox Interactive.', genero='Simulador, Gerenciamento', desenvolvedor='Colossal Order', foto_jogo='CitiesSkylines.jpg')
    jogo12 = Jogos(id= 12, nome='Child of Light', lancamento='2014', descricao='Child of Light é um jogo de RPG de plataforma desenvolvido pela Ubisoft Montreal.', genero='RPG, Plataforma', desenvolvedor='Ubisoft', foto_jogo='child_of_light.jpg')
    jogo13 = Jogos(id= 13, nome='Doki Doki Literature Club!', lancamento='2017', descricao='Doki Doki Literature Club! é um jogo eletrônico de visual novel desenvolvida pela Team Salvato.', genero='Visual Novel, Horror', desenvolvedor='Dan Salvato', foto_jogo='doki-doki.jpg')
    jogo14 = Jogos(id=14,nome='Persona 5', lancamento='2016', descricao='O jogo é cronologicamente a sexta edição da série Persona, que faz parte principalmente da franquia Megami Tensei.', genero='RPG,Social simulation game', desenvolvedor='Atlus', foto_jogo='persona_5.jpg')
    jogo15 = Jogos(id=15, nome='Grand Theft Auto V', lancamento='2013', descricao='Grand Theft Auto V é um jogo acompanha a história da campanha um jogador seguindo três criminosos e seus esforços para realizarem assaltos sob a pressão de uma agência governamental.', genero='Tiro, Mundo aberto', desenvolvedor='Rockstar Games', foto_jogo='GTA.jpg')
    jogo16 = Jogos(id=16, nome='The Legend of Zelda', lancamento='2017', descricao='Viaje pelos vastos campos, florestas e montanhas enquanto descobre o que aconteceu com o reino de Hyrule nesta deslumbrante aventura a céu aberto.', genero='RPG, Mundo aberto', desenvolvedor='Nintendo', foto_jogo='Zelda.jpg')
    lista_jogos = [jogo1, jogo2, jogo3, jogo4, jogo5, jogo6, jogo7, jogo8, jogo9, jogo10, jogo11, jogo12, jogo13, jogo14, jogo15, jogo16]

    for jogo in lista_jogos:
        database.session.add(jogo)
    database.session.commit()'''
    
    lista_jogos = Jogos.query.all()
    
    media1 = 0
    for jogo in lista_jogos:
        lista_aval1 = []
        lista_aval2 = []
        lista_aval3 = []
        lista_aval4 = []
        lista_aval5 = []
        lista_aval6 = []
        lista_aval7 = []
        lista_aval8 = []
        lista_aval9 = []
        lista_aval10 = []
        lista_aval11 = []
        lista_aval12 = []
        lista_aval13 = []
        lista_aval14 = []
        lista_aval15 = []
        lista_aval16 = []


        if jogo.id == 1:
            for aval1 in Avaliacao.query.filter_by(id_jogos=1).all():
                lista_aval1.append(aval1.avaliacao)
            if len(lista_aval1) == 0:
                media1 = None
            else:
                media1 = sum(lista_aval1)/len(lista_aval1)
                media1 = f'{media1:.1f}'
                jogo.media_jogos = float(media1)
                database.session.commit()
        elif jogo.id == 2:
            for aval1 in Avaliacao.query.filter_by(id_jogos=2).all():
                lista_aval2.append(aval1.avaliacao)
            if len(lista_aval2) == 0:
                media1 = None
            else:
                media1 = sum(lista_aval2)/len(lista_aval2)
                media1 = f'{media1:.1f}'
                jogo.media_jogos = float(media1)
                database.session.commit()
        elif jogo.id == 3:
            for aval1 in Avaliacao.query.filter_by(id_jogos=3).all():
                lista_aval3.append(aval1.avaliacao)
            if len(lista_aval3) == 0:
                media1 = None
            else:
                media1 = sum(lista_aval3)/len(lista_aval3)
                media1 = f'{media1:.1f}'
                jogo.media_jogos = float(media1)
                database.session.commit()
        elif jogo.id == 4:
            for aval1 in Avaliacao.query.filter_by(id_jogos=4).all():
                lista_aval4.append(aval1.avaliacao)
            if len(lista_aval4) == 0:
                media1 = None
            else:
                media1 = sum(lista_aval4)/len(lista_aval4)
                media1 = f'{media1:.1f}'
                jogo.media_jogos = float(media1)
                database.session.commit()
        elif jogo.id == 5:
            for aval1 in Avaliacao.query.filter_by(id_jogos=5).all():
                lista_aval5.append(aval1.avaliacao)
            if len(lista_aval5) == 0:
                media1 = None
            else:
                media1 = sum(lista_aval5)/len(lista_aval5)
                media1 = f'{media1:.1f}'
                jogo.media_jogos = float(media1)
                database.session.commit()
        elif jogo.id == 6:
            for aval1 in Avaliacao.query.filter_by(id_jogos=6).all():
                lista_aval6.append(aval1.avaliacao)
            if len(lista_aval6) == 0:
                media1 = None
            else:
                media1 = sum(lista_aval6)/len(lista_aval6)
                media1 = f'{media1:.1f}'
                jogo.media_jogos = float(media1)
                database.session.commit()
        elif jogo.id == 7:
            for aval1 in Avaliacao.query.filter_by(id_jogos=7).all():
                lista_aval7.append(aval1.avaliacao)
            if len(lista_aval7) == 0:
                media1 = None
            else:
                media1 = sum(lista_aval7)/len(lista_aval7)
                media1 = f'{media1:.1f}'
                jogo.media_jogos = float(media1)
                database.session.commit()
        elif jogo.id == 8:
            for aval1 in Avaliacao.query.filter_by(id_jogos=8).all():
                lista_aval8.append(aval1.avaliacao)
            if len(lista_aval8) == 0:
                media1 = None
            else:
                media1 = sum(lista_aval8)/len(lista_aval8)
                media1 = f'{media1:.1f}'
                jogo.media_jogos = float(media1)
                database.session.commit()
        elif jogo.id == 9:
            for aval1 in Avaliacao.query.filter_by(id_jogos=9).all():
                lista_aval9.append(aval1.avaliacao)
            if len(lista_aval9) == 0:
                media1 = None
            else:
                media1 = sum(lista_aval9)/len(lista_aval9)
                media1 = f'{media1:.1f}'
                jogo.media_jogos = float(media1)
                database.session.commit()
        elif jogo.id == 10:
            for aval1 in Avaliacao.query.filter_by(id_jogos=10).all():
                lista_aval10.append(aval1.avaliacao)
            if len(lista_aval10) == 0:
                media1 = None
            else:
                media1 = sum(lista_aval10)/len(lista_aval10)
                media1 = f'{media1:.1f}'
                jogo.media_jogos = float(media1)
                database.session.commit()
        elif jogo.id == 11:
            for aval1 in Avaliacao.query.filter_by(id_jogos=11).all():
                lista_aval11.append(aval1.avaliacao)
            if len(lista_aval11) == 0:
                media1 = None
            else:
                media1 = sum(lista_aval11)/len(lista_aval11)
                media1 = f'{media1:.1f}'
                jogo.media_jogos = float(media1)
                database.session.commit()
        elif jogo.id == 12:
            for aval1 in Avaliacao.query.filter_by(id_jogos=12).all():
                lista_aval12.append(aval1.avaliacao)
            if len(lista_aval12) == 0:
                media1 = None
            else:
                media1 = sum(lista_aval12)/len(lista_aval12)
                media1 = f'{media1:.1f}'
                jogo.media_jogos = float(media1)
                database.session.commit()
        elif jogo.id == 13:
            for aval1 in Avaliacao.query.filter_by(id_jogos=13).all():
                lista_aval13.append(aval1.avaliacao)
            if len(lista_aval13) == 0:
                media1 = None
            else:
                media1 = sum(lista_aval13)/len(lista_aval13)
                media1 = f'{media1:.1f}'
                jogo.media_jogos = float(media1)
                database.session.commit()
        elif jogo.id == 14:
            for aval1 in Avaliacao.query.filter_by(id_jogos=14).all():
                lista_aval14.append(aval1.avaliacao)
            if len(lista_aval14) == 0:
                media1 = None
            else:
                media1 = sum(lista_aval14)/len(lista_aval14)
                media1 = f'{media1:.1f}'
                jogo.media_jogos = float(media1)
                database.session.commit()
        elif jogo.id == 15:
            for aval1 in Avaliacao.query.filter_by(id_jogos=15).all():
                lista_aval15.append(aval1.avaliacao)
            if len(lista_aval15) == 0:
                media1 = None
            else:
                media1 = sum(lista_aval15)/len(lista_aval15)
                media1 = f'{media1:.1f}'
                jogo.media_jogos = float(media1)
                database.session.commit()
        elif jogo.id == 16:
            for aval1 in Avaliacao.query.filter_by(id_jogos=16).all():
                lista_aval16.append(aval1.avaliacao)
            if len(lista_aval6) == 0:
                media1 = None
            else:
                media1 = sum(lista_aval16)/len(lista_aval16)
                media1 = f'{media1:.1f}'
                jogo.media_jogos = float(media1)
                database.session.commit()


    if current_user.is_authenticated:
        foto_perfil = url_for('static', filename='foto_perfil/{}'.format(current_user.foto_perfil))
        return render_template('jogos.html', foto_perfil=foto_perfil, lista_jogos=lista_jogos, media1=media1)


@app.route('/jogos/<nome>', methods=['GET', 'POST'])
@login_required #precisa estar logado para acessar essa página
def avaliar(nome):
    form = Avaliacoes()
    lista_jogos = Jogos.query.all()

    for jogos in lista_jogos:
        if jogos.nome == nome:
            jogo = jogos

    lista_aval = []
    if jogo.id == 1:
        for aval1 in Avaliacao.query.filter_by(id_jogos=1).all():
            lista_aval.append(aval1.avaliacao)
    elif jogo.id == 2:
        for aval1 in Avaliacao.query.filter_by(id_jogos=2).all():
            lista_aval.append(aval1.avaliacao)
    elif jogo.id == 3:
        for aval1 in Avaliacao.query.filter_by(id_jogos=3).all():
            lista_aval.append(aval1.avaliacao)
    elif jogo.id == 4:
        for aval1 in Avaliacao.query.filter_by(id_jogos=4).all():
            lista_aval.append(aval1.avaliacao)
    elif jogo.id == 5:
        for aval1 in Avaliacao.query.filter_by(id_jogos=5).all():
            lista_aval.append(aval1.avaliacao)
    elif jogo.id == 6:
        for aval1 in Avaliacao.query.filter_by(id_jogos=6).all():
            lista_aval.append(aval1.avaliacao)
    elif jogo.id == 7:
        for aval1 in Avaliacao.query.filter_by(id_jogos=7).all():
            lista_aval.append(aval1.avaliacao)
    elif jogo.id == 8:
        for aval1 in Avaliacao.query.filter_by(id_jogos=8).all():
            lista_aval.append(aval1.avaliacao)
    elif jogo.id == 9:
        for aval1 in Avaliacao.query.filter_by(id_jogos=9).all():
            lista_aval.append(aval1.avaliacao)
    elif jogo.id == 10:
        for aval1 in Avaliacao.query.filter_by(id_jogos=10).all():
            lista_aval.append(aval1.avaliacao)
    elif jogo.id == 11:
        for aval1 in Avaliacao.query.filter_by(id_jogos=11).all():
            lista_aval.append(aval1.avaliacao)
    elif jogo.id == 12:
        for aval1 in Avaliacao.query.filter_by(id_jogos=12).all():
            lista_aval.append(aval1.avaliacao)
    elif jogo.id == 13:
        for aval1 in Avaliacao.query.filter_by(id_jogos=13).all():
            lista_aval.append(aval1.avaliacao)
    elif jogo.id == 14:
        for aval1 in Avaliacao.query.filter_by(id_jogos=14).all():
            lista_aval.append(aval1.avaliacao)
    elif jogo.id == 15:
        for aval1 in Avaliacao.query.filter_by(id_jogos=15).all():
            lista_aval.append(aval1.avaliacao)
    elif jogo.id == 16:
        for aval1 in Avaliacao.query.filter_by(id_jogos=16).all():
            lista_aval.append(aval1.avaliacao)

    if len(lista_aval) == 0:
        media = None
    else:
        media = sum(lista_aval)/len(lista_aval)
        media = f'{media:.1f}'
        jogo.media_jogos = float(media)
        database.session.commit()

    if form.validate_on_submit():
        aval = Avaliacao.query.filter_by(id_usuario=current_user.id, id_jogos=jogo.id).first()
        if aval:
            aval.avaliacao = form.avaliacao.data
            database.session.commit()
        else:
            avaliacao = Avaliacao(id_usuario=current_user.id, id_jogos=jogo.id, avaliacao=int(form.avaliacao.data))
            database.session.add(avaliacao)
            database.session.commit()

        return redirect(f'/jogos#{jogo.nome}') 

    elif request.method == 'GET':
        aval = Avaliacao.query.filter_by(id_usuario=current_user.id, id_jogos=jogo.id).first()
        if aval == None:
            pass
        else:
            form.avaliacao.data = aval.avaliacao

    if current_user.is_authenticated:
        foto_perfil = url_for('static', filename='foto_perfil/{}'.format(current_user.foto_perfil))
        return render_template('avaliar.html', foto_perfil=foto_perfil, form=form, jogo=jogo, media=media)

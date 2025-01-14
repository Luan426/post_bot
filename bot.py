import anilist
import telebot
import emoji
import animeBD
import traceback
from vndb import VNDB 
import translate
from telebot.types import InlineKeyboardButton,InlineKeyboardMarkup
from time import sleep
from threading import Thread
try:
    from secure import post_bot
    id_canal = post_bot.id_canal
    API_TOKEN = post_bot.API_TOKEN
    support = post_bot.support
except:
    import os
    id_canal = os.environ['ID_CANAL']
    API_TOKEN = os.environ['TOKEN']
    support = os.environ['SUPPORT']


import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

vn = VNDB('darkness_posting_bot', '0.1')

def icono(text=''):
    return emoji.emojize(text, use_aliases=True)


bot = telebot.TeleBot(API_TOKEN)
usercanal=bot.get_chat(id_canal).username

tipD = {'a': 'ANIME', 'm': 'MANGA','vn': 'NOVELA VISUAL'}
boton_empezar=icono('/Empezar')
t_i=icono('	:writing_hand: Ingrese el título de la multimedia a subir o presione /cancelar para salir.')
t_ty=icono(':white_check_mark: Seleccione la categoría en que se encuentra la multimedia.')
t_pre=icono('Hola {0} :wave:, este es un bot para ayudarte a publicar en el canal @{1}.\n\nPara comenzar presione :point_right: {2}')
boton_cancelar='/cancelar'
boton_sigui=icono('Siguiente :next_track_button:')
boton_selec=icono('Seleccionar :white_check_mark:')

salir_menu=icono(':house: Salir')
buscar_n=icono(':arrow_right_hook: Volver a buscar con otro texto')
t_cap=icono(':writing_hand: Escriba los cap o el fragmento que contiene el link/txt a subir.\n\n<code> cap 1 - cap 33</code>\n<code>Completo</code>\n<code>Primera parte</code>  etc)\n\no presione /cancelar para salir.')
t_l=icono(':link: Envíe el link o presione /finalizar')
t_el=icono(':dizzy_face: Error! Envíe el link/txt {0}')
t_at=icono(':memo: Envíe el archivo txt o presione /finalizar ')
t_li=icono(':dizzy_face: Link incorrecto por favor vuelva a enviarlo {0}')
t_ela=icono('Envíe el link :link: y/o el txt :memo: de la multimedia a subir.')
t_ad=icono(':expressionless: Lo sentimos, debe ser miembro del canal @{0} para poder usar el bot.\n\n/Empezar'.format(usercanal))

def acceso(id):
    m = bot.get_chat_member(id_canal, id).status
    # “creator”, “administrator”, “member”, “restricted”, “left” or “kicked”
    if m == 'member' or m == 'creator' or m == 'administrator':
        return True
    else:
        try:bot.send_message(id,t_ad)
        except:print(traceback.format_exc())
        return False

def inicio(id):
    if acceso(id):
        try:sms = bot.send_message(id, t_i)
        except:
            print(traceback.format_exc())
        bot.register_next_step_handler(sms, titulo)

def introducc(id,name):
    try:bot.send_message(id, t_pre.format(name,usercanal,boton_empezar))
    except:
        print(traceback.format_exc())
@bot.message_handler(commands=['start'])
def send_welcome(message):
    if not animeBD.get_u(message.chat.id):
        animeBD.new_u(message.chat.id,animeBD.Temp())

    introducc(message.chat.id,message.chat.first_name)

@bot.message_handler(commands=[boton_empezar[1:]])
def send_welcome(message):
    inicio(message.chat.id)

@bot.message_handler(commands=['bp'])
def send_welcome(message):
    status=bot.get_chat_member(id_canal, message.chat.id).status
    #print(status)
    if status=='creator' or status=='administrator':
        try:
            id=int(message.text[3:])
            if animeBD.del_post(id):
                try:bot.send_message(message.chat.id,"borrado")
                except:
                    print(traceback.format_exc())
                #tx_resumen()

            else:
                try:bot.send_message(message.chat.id,"error al borrar")
                except:
                    print(traceback.format_exc())
        except Exception as e:
            try:bot.send_message(message.chat.id,e)
            except:
                print(traceback.format_exc())
            print('comando bp',e)

@bot.message_handler(commands=['tx'])
def send_welcome(message):
    status=bot.get_chat_member(id_canal, message.chat.id).status
    #print(status)
    if status=='creator' or status=='administrator':
        #tx_resumen()
        try:bot.send_message(message.chat.id,'Resumen actualizado')
        except:
            print(traceback.format_exc())


def titulo(message):
    if message.text==boton_cancelar:
        introducc(message.chat.id,message.chat.first_name)
    else:
        temp=animeBD.get_temp(message.chat.id)
        if temp:
            temp.titulo=message.text
            temp.username=message.chat.username
            temp.id_user=message.chat.id
            temp.name=message.chat.first_name
            temp.post=animeBD.P_Anime()
            animeBD.set_temp(message.chat.id,temp)

            markup = InlineKeyboardMarkup()
            markup.row(InlineKeyboardButton('Anime', callback_data='a'))
            markup.row(InlineKeyboardButton('Manga', callback_data='m'))
            markup.row(InlineKeyboardButton('Novela Visual', callback_data='vn'))
            #markup.row(InlineKeyboardButton('Juego', callback_data='j'))
            markup.row(InlineKeyboardButton('Otro contenido', callback_data='o'))
            markup.row(InlineKeyboardButton(salir_menu, callback_data='s'))
            try:bot.send_message(message.chat.id, t_ty, reply_markup=markup)
            except:
                print(traceback.format_exc())
        else:introducc(message.chat.id,message.chat.first_name)

def error_Html(text):
    if type(text)== str:
        return text.replace('<','')
    else:return ''

@bot.message_handler(func=lambda m: True)
def echo_all(message):
    introducc(message.chat.id,message.chat.first_name)

def post_s(id,temp,index, kind):
    '''
        Crea la suguerencia de post
    '''
    if (temp.search):
        if kind == 'animanga':
            '''
            {'id': 30012,
                    'title': {'romaji': 'BLEACH'},
                    'format': 'MANGA',
                    'coverImage': {'large': 'https://s4.anilist.co/file/anilistcdn/media/manga/cover/medium/bx30012-z7U138mUaPdN.png'}}, {'id': 41330, 'title': {'romaji': 'Bleach Short Story Edition'}, 'format': 'ONE_SHOT', 'coverImage': {'large': 'https://s4.anilist.co/file/anilistcdn/media/manga/cover/medium/11330.jpg'}}
            '''
            t=temp.search[index]['title']['romaji']
            f=temp.search[index]['format']
            l=temp.search[index]['coverImage']['extraLarge']
        if kind == 'visualnovel':
            '''{'aliases': 'クラナド', 
            'image_nsfw': False, 
            'image': 'https://s2.vndb.org/cv/52/24252.jpg', 
            'id': 4, 
            'title': 'Clannad', 
            'image_flagging': {'sexual_avg': 0, 'violence_avg': 0, 'votecount': 10}, 
            'platforms': ['win', 'and', 'psp', 'ps2', 'ps3', 'ps4', 'psv', 'swi', 'vnd', 'xb3', 'mob'], 
            'length': 5, 
            'released': 
            '2004-04-28', 
            'original': None, 
            'languages': ['en', 'es', 'it', 'ja', 'ko', 'pt-br', 'ru', 'vi', 'zh'], 
            'orig_lang': ['ja'], 
            'links': {'renai': 'clannad', 'wikipedia': 'Clannad_(visual_novel)', 'wikidata': 'Q110607', 'encubed': 'clannad'}, 
            'description': 'Okazaki Tomoya is a third year high school student at Hikarizaka Private High School, leading a life full of resentment. His mother passed away in a car accident when he was young, leading his father, Naoyuki, to resort to alcohol and gambling to cope. This resulted in constant fights between the two until Naoyuki dislocated Tomoya’s shoulder. Unable to play on his basketball team, Tomoya began to distance himself from other people. Ever since he has had a distant relationship with his father, naturally becoming a delinquent over time.\n\nWhile on a walk to school, Tomoya meets a strange girl named Furukawa Nagisa, questioning if she likes the school at all. He finds himself helping her, and as time goes by, Tomoya finds his life heading towards a new direction.'}
            '''
            t=temp.search[index]['title']
            f='Novela Visual'
            l=temp.search[index]['image']

        capt = '<b>{0}\n\nFormato: {1}</b>'.format(error_Html(t), f)
        markup = InlineKeyboardMarkup()
        markup.row(InlineKeyboardButton(boton_sigui,
                                        callback_data='s^{0}^{1}'.format(index+1 if index<len(temp.search)-1 else 0, kind)),
                   InlineKeyboardButton(boton_selec,
                                        callback_data='i^{0}^{1}'.format(temp.search[index]['id'], kind))
                   )

        markup.row(InlineKeyboardButton(buscar_n,
                                        callback_data='b'))
        markup.row(InlineKeyboardButton(salir_menu,
                                        callback_data='s'))
        try:bot.send_photo(id,l, capt, parse_mode='html',reply_markup=markup)
        except:
            print(traceback.format_exc())
    else:
        try:bot.send_message(id ,'No se encontraron Resultados')
        except:
            print(traceback.format_exc())
        post_e(temp,id,markup_e())

def markup_e():
    markup = InlineKeyboardMarkup()
    markup.row(InlineKeyboardButton('Editar Título', callback_data='e^n'),
               InlineKeyboardButton('Editar Episodios', callback_data='e^e'))

    markup.row(InlineKeyboardButton('Editar Tipo', callback_data='e^t'),
               InlineKeyboardButton('Editar Formato', callback_data='e^f'))

    markup.row(InlineKeyboardButton('Editar Temporada', callback_data='e^m'),
               InlineKeyboardButton('Editar Audio', callback_data='e^a'))

    markup.row(InlineKeyboardButton('Editar Géneros', callback_data='e^g'),
               InlineKeyboardButton('Editar Estado', callback_data='e^s'))

    markup.row(InlineKeyboardButton('Editar Sinopsis', callback_data='e^i'),
               InlineKeyboardButton('Editar Imagen', callback_data='e^im'))

    markup.row(InlineKeyboardButton('Editar Información', callback_data='e^in'),
               InlineKeyboardButton(icono(':heavy_plus_sign: Más Categorías :heavy_plus_sign:'), callback_data='m^2'))


    markup.row(InlineKeyboardButton(salir_menu, callback_data='s'),InlineKeyboardButton(boton_sigui, callback_data='e^c'.format()))
    return markup

def markup_e1():
    markup = InlineKeyboardMarkup()
    markup.row(InlineKeyboardButton('Editar Tomo', callback_data='e^to'),
               InlineKeyboardButton('Editar Plataforma', callback_data='e^p'))

    markup.row(InlineKeyboardButton('Editar Estudio', callback_data='e^es'),
               InlineKeyboardButton('Editar Idioma', callback_data='e^id'))

    markup.row(InlineKeyboardButton('Editar Duración', callback_data='e^d'),
               InlineKeyboardButton('Editar Volumen', callback_data='e^v'))

    markup.row(InlineKeyboardButton('Editar Versión', callback_data='e^ve'),
               InlineKeyboardButton('Editar Peso', callback_data='e^pe'))

    markup.row(InlineKeyboardButton('Editar Creador', callback_data='e^cr'),
               InlineKeyboardButton('Editar Sis de Juego', callback_data='e^sj'))

    markup.row(InlineKeyboardButton('Hacer post anónimo', callback_data='e^anonymity'))

    markup.row(InlineKeyboardButton(icono(':heavy_plus_sign: Más Categorías :heavy_plus_sign:'), callback_data='m^1'))

    markup.row(InlineKeyboardButton(salir_menu, callback_data='s'),InlineKeyboardButton(boton_sigui, callback_data='e^c'.format()))
    return markup


def editar(message,t,temp):
    if message.text==boton_cancelar:
        introducc(message.chat.id,message.chat.first_name)
    else:
        if message.text=='/borrar':
            var=None
        else: var=error_Html(message.text)
        if message.content_type == 'text':

            if t=='n':
                temp.post.titulo=var
            elif t=='e':
                temp.post.episodes = var
            elif t=='m':
                temp.post.temporada=var
            elif t=='a':
                temp.post.audio=var
            elif t=='g':
                temp.post.genero=var
            elif t=='s':
                temp.post.status=var
            elif t=='i':
                temp.post.descripcion=var
            elif t=='t':
                temp.post.tipo=var
            elif t=='f':
                temp.post.format=var
            elif t=='in':
                temp.post.inf=var
            elif t=='to':
                temp.post.tomos=var
            elif t=='p':
                temp.post.plata=var
            elif t=='es':
                temp.post.estudio=var
            elif t=='id':
                temp.post.idioma=var
            elif t=='d':
                temp.post.duracion=var
            elif t=='v':
                temp.post.volumen=var
            elif t=='ve':
                temp.post.version=var
            elif t=='pe':
                temp.post.peso=var
            elif t=='cr':
                temp.post.creador=var
            elif t=='sj':
                temp.post.sis_j=var
            elif t=='im':
                temp.post.imagen=None
            elif t=='anonymity':
                if var=='/si':
                    temp.hidden_name = temp.username if temp.username else temp.name
                    temp.username = None
                    temp.name = None

        elif t=='im' and message.content_type == 'photo':
            temp.post.imagen = message.photo[0].file_id


        animeBD.set_temp(message.chat.id,temp)
        post_e(temp,message.chat.id,temp.markup if temp.markup else markup_e())


def post_e(temp,id,markup=None):
    tt=[]
    def aj(txt,var):
        if var:tt.append( txt.format(var))

    tit=':radioactive:{0} {1}\n\n'.format(
        '({0})'.format(temp.post.tipo[0]) if temp.post.tipo else '',
        '<b>{0}</b>'.format(temp.post.titulo) if temp.post.titulo else ':expressionless:')

    tt.append(tit)
    aj(':heavy_check_mark:Tipo: <b>{0}</b>\n',temp.post.tipo)
    aj(':heavy_check_mark:Formato: <b>{0}</b>\n',temp.post.format)
    aj(':heavy_check_mark:Episodios: <b>{0}</b>\n', temp.post.episodes)
    aj(':heavy_check_mark:Temporada: <b>{0}</b>\n', temp.post.temporada)
    aj(':heavy_check_mark:Tomo: <b>{0}</b>\n', temp.post.tomos)
    aj(':heavy_check_mark:Volumen: <b>{0}</b>\n', temp.post.volumen)
    aj(':heavy_check_mark:Plataforma: <b>{0}</b>\n', temp.post.plata)
    aj(':notes:Audio: <b>{0}</b>\n', temp.post.audio)
    aj(':heavy_check_mark:Idioma: <b>{0}</b>\n', temp.post.idioma)
    aj(':hourglass_flowing_sand:Duración: <b>{0}</b>\n', temp.post.duracion)
    aj(':heavy_check_mark:Géneros: <b>{0}</b>\n',
       ', '.join(temp.post.genero) if type(temp.post.genero)==list else temp.post.genero)
    aj(':heavy_check_mark:Tags: <b>{0}</b>\n',
       ', '.join(temp.post.tags) if type(temp.post.tags)==list else temp.post.tags)
    aj(':heavy_check_mark:Estudio: <b>{0}</b>\n', temp.post.estudio)
    aj(':heavy_check_mark:Sistema de juego: <b>{0}</b>\n', temp.post.sis_j)
    aj(':floppy_disk:Peso: <b>{0}</b>\n', temp.post.peso)
    aj(':heavy_check_mark:Versión: <b>{0}</b>\n', temp.post.version)
    aj(':heavy_check_mark:Creador: <b>{0}</b>\n', temp.post.creador)
    aj(':heavy_check_mark:Año: <b>{0}</b>\n', temp.post.year)
    aj(':heavy_check_mark:Estado: <b>{0}</b>\n', temp.post.status)
    aj('\n:beginner:Sinopsis: <b>{0}</b>\n', '{0}...'.format(temp.post.descripcion[:500]) if temp.post.descripcion and len(temp.post.descripcion) > 200 else temp.post.descripcion)
    aj('\n\n:warning:Información: <b>{0}</b>\n', temp.post.inf)
    tt.append('\n:star:Aporte #{0} de {1}'.format(
        animeBD.get_aport(temp.id_user)+1,('@' if temp.username else '') + (temp.username if temp.username else temp.name if temp.name else 'Anónimo')))
    if temp.post.link:tt.append('\n\n:link:Link: <a href="{0}"><b>{1}</b></a>'.format(temp.post.link,temp.post.episo_up))

    capt = icono(''.join(tt))
    try:
        if temp.post.imagen:
            try:
                vvvv=bot.send_photo(id, temp.post.imagen, capt, parse_mode='html', reply_markup=markup).id
            except:
                print(traceback.format_exc())
            return vvvv
        else:
            try:vvvv=bot.send_message(id, capt, parse_mode='html', reply_markup=markup,disable_web_page_preview=True).id
            except:
                print(traceback.format_exc())
            return vvvv
    except:print(traceback.format_exc())


def txtlink(message,temp):
    def finalizar():
        id_sms = post_e(temp, id_canal)
        if temp.post.txt:
            try:bot.send_document(id_canal, temp.post.txt,caption='{0}\n{1}\n(<a href="https://tg.i-c-a.su/media/{2}/{3}">Link Para Delta</a>)'.format(temp.post.episo_up,temp.post.name_txt,usercanal,id_sms+1),parse_mode='html')
            except:
                print(traceback.format_exc())
        try:
            bot.send_message(message.chat.id, icono('<a href="https://t.me/{0}/{1}">:white_check_mark: <b>Enviado al canal :exclamation:</b></a>\n\nPresione {2} para crear otro post.'.format(usercanal,id_sms,boton_empezar)),parse_mode='html',disable_web_page_preview=True)
            if temp.hidden_name:
                try:
                    bot.send_message(support, '@' + temp.hidden_name + f'<a href="https://t.me/{usercanal}/{id_sms}"> ha usado el modo anónimo</a>',parse_mode='html',disable_web_page_preview=True)
                except:
                    print(traceback.format_exc())
        except:
            print(traceback.format_exc())
        animeBD.aport(message.chat.id)
        animeBD.new_p(id_sms,message.chat.id,temp.post.titulo)
        #tx_resumen()

    if message.text=='/finalizar':
        finalizar()
    elif message.text=='/cancelar':
        introducc(message.chat.id,message.chat.first_name)

    elif message.content_type == 'text':
        if 'HTTP://' in message.text.upper() or 'HTTPS://' in message.text.upper() :
            temp.post.link=message.text
            animeBD.set_temp(message.chat.id, temp)
            if  temp.post.txt:
                finalizar()
            else:
                try:sms = bot.send_message(message.chat.id, t_at)
                except:
                    print(traceback.format_exc())
                bot.register_next_step_handler(sms, txtlink, temp)

        else:
            try:sms=bot.send_message(message.chat.id,t_li.format(
                'o presione /finalizar' if temp.post.link or temp.post.txt else ''))
            except:
                print(traceback.format_exc())
            bot.register_next_step_handler(sms, txtlink, temp)
    elif message.content_type == "document":
        temp.post.txt = message.document.file_id
        temp.post.name_txt=message.document.file_name
        animeBD.set_temp(message.chat.id, temp)
        if  temp.post.link:
            finalizar()
        else:
            try:sms = bot.send_message(message.chat.id, t_l)
            except:
                print(traceback.format_exc())
            bot.register_next_step_handler(sms, txtlink, temp)
    else:
        try:sms = bot.send_message(message.chat.id, t_el.format(
            'o presione /finalizar' if temp.post.link or temp.post.txt else '' ))
        except:
            print(traceback.format_exc())
        bot.register_next_step_handler(sms, txtlink, temp)


def capsub(message,temp):
    if message.text==boton_cancelar:
        introducc(message.chat.id,message.chat.first_name)
    else:
        temp.post.episo_up=error_Html(message.text)
        animeBD.set_temp(message.chat.id,temp)
        try:sms = bot.send_message(message.chat.id, t_ela)
        except:
            print(traceback.format_exc())
        bot.register_next_step_handler(sms, txtlink,temp)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    try:
        bot.delete_message(call.from_user.id, call.message.message_id)
    except Exception as e:
            print('error borrar\n{0}'.format(e))

    else:
        temp=animeBD.get_temp(call.from_user.id)
        if temp:
            data = call.data.split('^')
            l=len(data)
            if l==1:
                temp.tipo=data[0]

                if data[0]=='s':
                    introducc(call.from_user.id,call.from_user.first_name)
                elif data[0]=='b':
                    inicio(call.from_user.id)

                else:
                    if data[0]=='a' or data[0]=='m':
                        d = anilist.search(temp.titulo, data[0])
                        temp.search=d
                        post_s(call.from_user.id,temp,0,'animanga')
                    elif data[0]=='vn':
                        d = vn.get('vn', 'basic,details', f'(title~"{temp.titulo}")', '')
                        temp.search = [item for item in d['items']]
                        post_s(call.from_user.id,temp,0,'visualnovel')
                    elif data[0]=='o':
                        temp.post.titulo=error_Html(temp.titulo)
                        post_e(temp, call.from_user.id, markup_e())

                    animeBD.set_temp(call.from_user.id, temp)



            elif l==3:
                if data[0]=='s':
                    post_s(call.from_user.id,temp,int(data[1]), data[2])
                elif data[0]=='i':
                    if data[2] == 'animanga':
                        p=anilist.get(data[1])
                        """{'coverImage': 'https://s4.anilist.co/file/anilistcdn/media/manga/cover/medium/bx30106-GgFOXeyB70xj.png', 
                        'title': 'Cardcaptor Sakura', 
                        'format': 'MANGA', 
                        'status': 'FINISHED', 
                        'episodes': None, 
                        'genres': ['#Adventure', '#Comedy', '#Fantasy', '#Mahou Shoujo', '#Romance'], 
                        'description': 'El cuarto grado Sakura Kinomoto encuentra un libro ...)'}"""
                        temp.search=None
                        temp.titulo=''

                        temp.post = animeBD.P_Anime()
                        temp.post.tipo = tipD[temp.tipo]
                        temp.tipo=''
                        temp.post.imagen=p['coverImage']
                        temp.post.titulo=error_Html(p['title'])
                        temp.post.format=p['format']
                        temp.post.status=p['status']
                        temp.post.episodes=p['episodes']
                        temp.post.genero=p['genres']
                        temp.post.tags=p['tags']
                        temp.post.year=p['year']
                        temp.post.descripcion=error_Html(p['description'])
                    if data[2]=='visualnovel':
                        p=vn.get('vn','basic,details',f'(id={data[1]})','')['items'][0]
                        '''{'aliases': 'クラナド', 
                        'image_nsfw': False, 
                        'image': 'https://s2.vndb.org/cv/52/24252.jpg', 
                        'id': 4, 
                        'title': 'Clannad', 
                        'image_flagging': {'sexual_avg': 0, 'violence_avg': 0, 'votecount': 10}, 
                        'platforms': ['win', 'and', 'psp', 'ps2', 'ps3', 'ps4', 'psv', 'swi', 'vnd', 'xb3', 'mob'], 
                        'length': 5, 
                        'released': 
                        '2004-04-28', 
                        'original': None, 
                        'languages': ['en', 'es', 'it', 'ja', 'ko', 'pt-br', 'ru', 'vi', 'zh'], 
                        'orig_lang': ['ja'], 
                        'links': {'renai': 'clannad', 'wikipedia': 'Clannad_(visual_novel)', 'wikidata': 'Q110607', 'encubed': 'clannad'}, 
                        'description': 'Okazaki Tomoya is a third year high school student at Hikarizaka Private High School, leading a life full of resentment. His mother passed away in a car accident when he was young, leading his father, Naoyuki, to resort to alcohol and gambling to cope. This resulted in constant fights between the two until Naoyuki dislocated Tomoya’s shoulder. Unable to play on his basketball team, Tomoya began to distance himself from other people. Ever since he has had a distant relationship with his father, naturally becoming a delinquent over time.\n\nWhile on a walk to school, Tomoya meets a strange girl named Furukawa Nagisa, questioning if she likes the school at all. He finds himself helping her, and as time goes by, Tomoya finds his life heading towards a new direction.'},
                        '''
                        temp.search=None
                        temp.titulo=''

                        temp.post = animeBD.P_Anime()
                        temp.post.tipo = tipD[temp.tipo]
                        temp.tipo=''
                        temp.post.imagen=p['image']
                        temp.post.idioma='‼editar'
                        temp.post.plata='‼editar'
                        temp.post.titulo=error_Html(p['title'])
                        temp.post.descripcion=translate.traducir(error_Html(p['description']))

                    animeBD.set_temp(call.from_user.id,temp)

                    post_e(temp,call.from_user.id,markup_e())

            elif l==2:
                if data[0]=='e':
                    if data[1]=='c':

                        try:sms = bot.send_message(call.from_user.id, t_cap,parse_mode='html')
                        except:
                            print(traceback.format_exc())
                        bot.register_next_step_handler(sms, capsub,temp)
                    elif data[1]=='anonymity':
                        try:sms=bot.send_message(call.from_user.id, '😑 aunque la comunidad no lo vea, los admins si, no lo intentes usar para el mal\n /si    /no')
                        except:
                            print(traceback.format_exc())
                        bot.register_next_step_handler(sms, editar,data[1],temp )
                    else:
                        try:sms=bot.send_message(call.from_user.id, 'Envíe los nuevos datos o presione /borrar para borrar esa categoría.')
                        except:
                            print(traceback.format_exc())
                        bot.register_next_step_handler(sms, editar,data[1],temp )
                elif data[0]=='m':
                    markup=None
                    if data[1]=='1':markup=markup_e()
                    else:markup=markup_e1()
                    temp.markup=markup
                    animeBD.set_temp(call.from_user.id,temp)
                    post_e(temp, call.from_user.id,markup)


        else:introducc(call.from_user.id,call.from_user.first_name)

def tx_resumen():
    #id_sms,titulo

    p=animeBD.get_resumen()
    posts=[]
    id=0
    for pp in p:
        posts.append('<a href="http://t.me/{0}/{1}">:radioactive: <b>{2}</b></a>'.format(usercanal,pp[0],pp[1]))
    if posts:
        def new_post(texto):
            try:id = bot.send_message(id_canal, texto, parse_mode='html', disable_web_page_preview=True).id
            except:
                print(traceback.format_exc())
            animeBD.set_id_re(id)
            return id

        texto=icono('<b><u>Resumen (24 horas):</u></b>\n\n{0}'.format('\n\n'.join(posts)))

        id_antiguo=animeBD.get_id_re()
        if id_antiguo:
            try:
                id=bot.edit_message_text(texto,id_canal,id_antiguo,parse_mode='html',disable_web_page_preview=True).id
            except Exception as e:
                print(e)
                if 'Bad Request: message to edit not found' in str(e) or 'MESSAGE_ID_INVALID' in str(e):
                    id=new_post(texto)
                else:id=id_antiguo
        else:id=new_post(texto)
        #bot.unpin_chat_message(id_canal,id)
        try:bot.pin_chat_message(id_canal,id,disable_notification=True)
        except Exception as e:print('pin resumen',e)


def hilo_time():

    while True:
        sleep(3600)
        g = Thread(target=tx_resumen)
        g.start()


def inicio_bot():
    if usercanal and API_TOKEN and id_canal:
        #g = Thread(target=hilo_time)
        #g.start()
        print('-----------------------\nBot iniciado\n-----------------------')
        #tx_resumen()
        try:
            bot.polling(none_stop=True)
        except:print(traceback.format_exc())

if __name__ == '__main__':inicio_bot()

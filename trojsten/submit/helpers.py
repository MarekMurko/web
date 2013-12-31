# -*- coding: utf-8 -*-
from django.conf import settings
from time import time
import os
import random
import socket
import xml.etree.ElementTree as ET


def write_file(what, where):
    '''Vytvorí cieľový adresár a uloží string do súboru.'''
    try:
        os.makedirs(where.rsplit('/', 1)[0])
    except:
        pass
    with open(where, 'w+') as destination:
        destination.write(what)


def save_file(what, where):
    '''Vytvorí cieľový adresár a uloží stiahnutý súbor.'''
    try:
        os.makedirs(where.rsplit('/', 1)[0])
    except:
        pass
    with open(where, 'wb+') as destination:
        for chunk in what.chunks():
            destination.write(chunk)


def get_lang_from_filename(filename):
    ext = os.path.splitext(filename)[1].lower()
    extmapping = {
        ".cpp": ".cc",
        ".cc":  ".cc",
        ".pp":  ".pas",
        ".pas": ".pas",
        ".dpr": ".pas",
        ".c":   ".c",
        ".py":  ".py",
        ".py3": ".py3",
        ".hs":  ".hs",
        ".cs":  ".cs",
        ".java": ".java"}

    if not ext in extmapping:
        return False
    return extmapping[ext]


def get_path_raw(contest_id, task_id, user_id):
    '''Vypočíta cestu, kam uložiť súbory submitu bez dotknutia databázy.

    Cesta má tvar: $SUBMIT_PATH/submits/KSP/task_id/user_id
    '''

    return "%s/submits/%s/%s/%s" % (
        settings.SUBMIT_PATH,
        str(contest_id),
        str(task_id),
        str(user_id))


def get_path(task, user):
    '''Vypočíta cestu, kam uložiť súbory submitu.

    Cesta má tvar: $SUBMIT_PATH/submits/KSP/task_id/user_id
    '''
    return get_path_raw(task.round.series.competition.name, task.id, user.id)


def post_submit(raw):
    '''Pošle RAW na otestovanie'''
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((settings.TESTER_URL, settings.TESTER_PORT))
    sock.send(raw)
    sock.close()


def process_submit_raw(f, contest_id, task_id, language, user_id):
    '''Spracuje submit bez dotknutia databázy'''
    # Determine language from filename if language not entered
    if language == '.':
        lang = get_lang_from_filename(f.name)
        if not lang:
            return False
        language = lang

    # Generate submit ID
    # Submit ID is <timestamp>-##### where ##### are 5 random digits
    timestamp = int(time())
    submit_id = str(timestamp) + '-'
    for i in range(0, 5):
        submit_id += str(random.randint(0, 9))

    # Determine local directory to store RAW file into
    path = get_path_raw(contest_id, task_id, user_id)

    # Prepare submit parameters (not entirely sure about this yet).
    user_id = contest_id + '-' + str(user_id)
    task_id = contest_id + '-' + str(task_id)
    original_name = f.name
    correct_filename = task_id + language
    data = f.read()

    # Prepare RAW from submit parameters
    raw = "%s\n%s\n%s\n%s\n%s\n%s\n%s" % (
        contest_id,
        submit_id,
        user_id,
        correct_filename,
        timestamp,
        original_name,
        data)

    # Write RAW to local file
    write_file(raw, path + '/' + submit_id + '.raw')

    # Send RAW for testing (uncomment when deploying)
    # post_submit(raw)

    # Return submit ID
    return submit_id


def process_submit(f, task, language, user):
    '''Načíta všetko potrebné z databázy a spracuje submit'''
    contest_id = task.round.series.competition.name
    return process_submit_raw(f, contest_id, task.id, language, user.id)


def update_submit(submit):
    '''Zistí, či už je dotestované, ak hej, tak updatne databázu.

    Ak je dotestované, tak do zložky so submitmi testovač nahral súbor
    s rovnakým názvom ako má submit len s príponou .protokol

    Tento súbor obsahuje výstup testovača (v XML) a treba ho parse-núť
    '''
    protocol_path = submit.filepath.rsplit('.', 1)[0] + '.protokol'
    if os.path.exists(protocol_path):
        tree = ET.parse(protocol_path)
        # Ak kompilátor vyhlási chyby, testovač ich vráti v tagu <compileLog>
        # Ak takýto tag existuje, výsledok je chyba pri testovaní a 0 bodov.
        clog = tree.find("compileLog")
        if clog is not None:
            result = 'CERR'
            points = 0
        else:
            # Pre každý vstup kompilátor vyprodukuje tag <test>, všetky <test>-y
            # sú v tag-u <runLog>. Výsledok je buď OK, alebo prvý nájdený druh
            # chyby.
            runlog = tree.find("runLog")
            result = 'OK'
            for test in runlog:
                if test.tag != 'test':
                    continue
                test_result = test[2].text
                if test_result != 'OK':
                    result = test_result
                    break
            # Na konci testovača je v tagu <score> uložené percento získaných
            # bodov.
            score = int(float(tree.find("runLog/score").text))
            points = (submit.task.source_points * score) // 100
        submit.points = points
        submit.tester_response = result
        submit.testing_status = 'finished'
        submit.save()

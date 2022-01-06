from genericpath import exists
import os
import re
import datetime
import time
import shutil
from pprint import pprint
import click
import sqlite3

@click.command()
@click.option("--top-dir", required=True,
    help="Defines the top of the tree.. ")
@click.option("--create-list", "-c", is_flag=True,
    help="Create folder list file.")
#@click.option("--dry-run", is_flag=True,
#    help="Act as if folders were deleted")
@click.option("--delete", "-d", is_flag=True,)
def main(top_dir, create_list, delete):
    folder_list_file = "./folder-list.db"
    if (create_list):
        if exists(folder_list_file):
            click.echo("folder-list.db does already exist.")
            exit(-1)
        else:
            con = sqlite3.connect(folder_list_file)
            with con:
                cur = con.cursor()
                cur.execute("CREATE TABLE folder_list(folder text not null, deleted bool)")
                con.commit()
                find_folders_to_delete(cur, top_dir)
                con.commit()
    if (delete):
        print("Es wird gelöscht..")
        if not exists(folder_list_file):
            click.echo("folder-list.db existriert noch nicht. Bitte mit Option -c erstellen")
            exit(-1)
        else:
            con = sqlite3.connect(folder_list_file)
            with con:
                cur = con.cursor()
                cur.execute("SELECT COUNT(*) FROM `folder_list`")
                row_count, *_ = cur.fetchone()
                pprint(f"row_count: {row_count}")
                cur.execute("SELECT COUNT(*) FROM `folder_list` WHERE `deleted` = 1",) # 1 = True
                already_deleted, *_ = cur.fetchone()
                pprint(f"already_deleted: {already_deleted}")
                click.echo(f"{already_deleted}/{row_count} were already deleted. Progrssing now")
                pending :int = int(row_count) - int(already_deleted)
                cur.execute("SELECT rowid, folder FROM `folder_list` WHERE `deleted` = 0") # 0 = False
                remaining_list = cur.fetchall()
                so_far = 0
                for id, item in remaining_list:
                    click.echo(f"id {id} :: item:{item}")
                    if os.path.exists(item):
                        so_far += 1
                        shutil.rmtree(item, onerror=del_logger)
                        click.echo(f"{so_far}/{pending}")
                        cur.execute(f"UPDATE folder_list SET deleted = 1 WHERE rowid = {id}") # 1 = True
                        con.commit()
                        #print("Waiting 1s..")
                        #time.sleep(1)


def del_logger(func, path, error):
    with open('./logger.log', "a+", encoding="utf-8") as f:
        # poor man's logging
        print(f"{datetime.datetime.now()} path: {path} -- error: {error}")
        print(f"{datetime.datetime.now()} path: {path} -- error: {error}", file=f)


    





def walk(top, maxdepth):
    "Scannt den Verzeichnisbaum vollständig und gibt die obersten Verzeichnisse zurück"
    dirs, nondirs = [], []
    for entry in os.scandir(top):
        (dirs if entry.is_dir() else nondirs).append(entry.path)
    yield top #, dirs, nondirs
    if maxdepth > 1:
        for path in dirs:
            for x in walk(path, maxdepth-1):
                yield x


def find_folders_to_delete(db_cur, top_dir):
    "finds the folders "
    for x in walk(top_dir, 6):
        #pure_top = os.path.basename(os.path.normpath(top))
        #if re.match("!(^\d{5}\b.*$)", pure_top):
        # verwende nur projektnummern, die kleiner sind als 42000 und > 20.000
        m_result = re.match("^(2\d{1}|3\d{1}|40|41)\d{3}_.*", os.path.basename(os.path.normpath(x)))
        if m_result:
            modification_year = time.strftime('%Y', time.localtime(os.path.getmtime(x)))
            # ignoriere alle, die neuer sind als 2016
            if int(modification_year) < 2019:
                #list_all.append(x)
                #list_all.append(modification_year)
                    print(f"{x} | {modification_year}")
                    db_cur.execute("INSERT INTO `folder_list` (folder, deleted) VALUES (?,?)", [x,False])

def dry_runs(folder_list_file):
    pass



if __name__ == "__main__":
    main()
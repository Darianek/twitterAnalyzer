import os
import time
import json
import pandas as pd

from twitter_data_conversion import *
from twitter_get_user import get_user


def get_stats(screen_name, access_file, nodeDataFrame, edgeDataFrame):

    uid = []
    lbl = []
    focnt = []
    frcnt = []
    lct = []
    cra = []
    prtd = []
    verified = []
    lstcnt = []
    favcnt = []
    statcnt = []
    dftprl = []
    dftimg = []

    esid = []
    etid = []
    directed = []

    counter = 0

    client, followers, friends, people = get_user(screen_name, access_file)
    current_user = client.get_user(screen_name)
    users_done = set()
    if current_user.protected:
        if current_user.id not in uid:
            uid.append(str(current_user.id))
            lbl.append(screen_name)
            focnt.append(str(0))
            frcnt.append(str(current_user.friends_count))
            if isinstance(current_user.created_at, datetime):
                strDate = str(current_user.created_at.strftime('%a %b %d %H:%M:%S +%f %Y'))
                objDate = datetime.strptime(strDate, '%a %b %d %H:%M:%S +%f %Y')
            else:
                strDate = str(current_user.created_at)
                objDate = datetime.strptime(strDate, '%a %b %d %H:%M:%S +%f %Y')
            cra.append(objDate)
            prtd.append(str(current_user.protected))
            lct.append(False)
            verified.append(current_user.verified)
            lstcnt.append(current_user.listed_count)
            favcnt.append(current_user.favourites_count)
            statcnt.append(current_user.statuses_count)
            dftprl.append(current_user.default_profile)
            dftimg.append(current_user.default_profile_image)
    else:
        try:
            if current_user.id not in uid:
                uid.append(str(current_user.id))
                lbl.append(screen_name)
                focnt.append(str(current_user.followers_count))
                frcnt.append(str(current_user.friends_count))
                if isinstance(current_user.created_at, datetime):
                    strDate = str(current_user.created_at.strftime('%a %b %d %H:%M:%S +%f %Y'))
                    objDate = datetime.strptime(strDate, '%a %b %d %H:%M:%S +%f %Y')
                else:
                    strDate = str(current_user.created_at)
                    objDate = datetime.strptime(strDate, '%a %b %d %H:%M:%S +%f %Y')
                cra.append(objDate)
                prtd.append(str(current_user.protected))
                verified.append(current_user.verified)
                lstcnt.append(current_user.listed_count)
                favcnt.append(current_user.favourites_count)
                statcnt.append(current_user.statuses_count)
                dftprl.append(current_user.default_profile)
                dftimg.append(current_user.default_profile_image)
                if current_user.location:
                    lct.append(True)
                else:
                    lct.append(False)
        except json.decoder.JSONDecodeError:
            if current_user.id not in uid:
                uid.append(str(current_user.id))
                lbl.append(screen_name)
                focnt.append(str(current_user.followers_count))
                frcnt.append(str(current_user.friends_count))
                if isinstance(current_user.created_at, datetime):
                    strDate = str(current_user.created_at.strftime('%a %b %d %H:%M:%S +%f %Y'))
                    objDate = datetime.strptime(strDate, '%a %b %d %H:%M:%S +%f %Y')
                else:
                    strDate = str(current_user.created_at)
                    objDate = datetime.strptime(strDate, '%a %b %d %H:%M:%S +%f %Y')
                cra.append(objDate)
                prtd.append(str(current_user.protected))
                lct.append(False)
                verified.append(current_user.verified)
                lstcnt.append(current_user.listed_count)
                favcnt.append(current_user.favourites_count)
                statcnt.append(current_user.statuses_count)
                dftprl.append(current_user.default_profile)
                dftimg.append(current_user.default_profile_image)
    counter += 1

    for someone in followers:
        follower = json.loads(someone)
        esid.append(str(follower['id']))
        etid.append(str(current_user.id))
        directed.append('Directed')
    for someone in friends:
        friend = json.loads(someone)
        esid.append(str(current_user.id))
        etid.append(str(friend['id']))
        directed.append('Directed')

    edgeDict = {'Source': esid, 'Target': etid, 'Direction': directed}

    newEdgeDataframe = pd.DataFrame(edgeDict)
    edgeDataFrame = edgeDataFrame.append(newEdgeDataframe, ignore_index=True)

    current_labels = list(nodeDataFrame['Label'].values)
    for someone in people:
        person = json.loads(someone)
        if person['screen_name'] not in current_labels:
            uid.append(str(person['id']))
            lbl.append(person['screen_name'])
            focnt.append(str(person['followers_count']))
            frcnt.append(str(person['friends_count']))
            if isinstance(person['created_at'], datetime):
                strDate = str(person['created_at'].strftime('%a %b %d %H:%M:%S +%f %Y'))
                objDate = datetime.strptime(strDate, '%a %b %d %H:%M:%S +%f %Y')
            else:
                strDate = str(person['created_at'])
                objDate = datetime.strptime(strDate, '%a %b %d %H:%M:%S +%f %Y')
            cra.append(objDate)
            prtd.append(str(person['protected']))
            verified.append(person['verified'])
            lstcnt.append(person['listed_count'])
            favcnt.append(person['favourites_count'])
            statcnt.append(person['statuses_count'])
            dftprl.append(person['default_profile'])
            dftimg.append(person['default_profile_image'])
            if person['location']:
                lct.append(True)
            else:
                lct.append(False)
            users_done.add(person['screen_name'])

    nodeDict = {'Id': uid, 'Label': lbl, 'Followers Count': focnt, 'Friends Count': frcnt,
                'Created at': cra, 'Protected': prtd, 'Location': lct, 'Verified': verified,
                'Listed count': lstcnt, 'Favorites count': favcnt, 'Status count': statcnt,
                'Default profile': dftprl, 'Default profile image': dftimg}

    newNodeDataFrame = pd.DataFrame(nodeDict)
    nodeDataFrame = nodeDataFrame.append(newNodeDataFrame, ignore_index=True)
    
    return nodeDataFrame, edgeDataFrame

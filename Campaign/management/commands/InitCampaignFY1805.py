from hashlib import md5

from django.contrib.auth.models import User, Group
from django.core.management.base import BaseCommand, CommandError

from Campaign.models import CampaignTeam
from EvalData.models import Market, Metadata

X_LANGUAGES = (
  'ara', 'deu', 'fra', 'hin', 'ita', 'jpn', 'kor', 'por', 'rus', 'spa', 'zho'
)

CAMPAIGN_NAME = 'AppenEval20171024'
CAMPAIGN_KEY = '20171024'
CAMPAIGN_NO = 5
ANNOTATORS = 5
TASKS = 10
REDUNDANCY = 1

# pylint: disable=C0111,C0330,E1101
class Command(BaseCommand):
    help = 'Initialises campaign FY18 #5'

    def handle(self, *args, **options):
        # Find super user
        superusers = User.objects.filter(is_superuser=True)
        if not superusers.exists():
            _msg = 'Failure to identify superuser'
            self.stdout.write(_msg)
            return

        _msg = 'Identified superuser: {0}'.format(superusers[0])
        self.stdout.write(_msg)

        # Create Market and Metadata instances for all language pairs
        for code in X_LANGUAGES:
            # EX
            _ex_market = Market.objects.filter(
              sourceLanguageCode='eng',
              targetLanguageCode=code,
              domainName='AppenFY18'              
            )

            if not _ex_market.exists():
                _ex_market = Market.objects.get_or_create(
                  sourceLanguageCode='eng',
                  targetLanguageCode=code,
                  domainName='AppenFY18',
                  createdBy=superusers[0]
                )
                _ex_market = _ex_market[0]

            else:
                _ex_market = _ex_market.first()

            _ex_meta = Metadata.objects.filter(
              market=_ex_market,
              corpusName='AppenFY18',
              versionInfo='1.0',
              source='official'             
            )

            if not _ex_meta.exists():
                _ex_meta = Metadata.objects.get_or_create(
                  market=_ex_market,
                  corpusName='AppenFY18',
                  versionInfo='1.0',
                  source='official',
                  createdBy=superusers[0]
                )
                _ex_meta = _ex_meta[0]

            else:
                _ex_meta = _ex_meta.first()

            # XE
            _xe_market = Market.objects.filter(
              sourceLanguageCode=code,
              targetLanguageCode='eng',
              domainName='AppenFY18'              
            )

            if not _xe_market.exists():
                _xe_market = Market.objects.get_or_create(
                  sourceLanguageCode=code,
                  targetLanguageCode='eng',
                  domainName='AppenFY18',
                  createdBy=superusers[0]
                )
                _xe_market = _xe_market[0]

            else:
                _xe_market = _xe_market.first()

            _xe_meta = Metadata.objects.filter(
              market=_xe_market,
              corpusName='AppenFY18',
              versionInfo='1.0',
              source='official'             
            )

            if not _xe_meta.exists():
                _xe_meta = Metadata.objects.get_or_create(
                  market=_xe_market,
                  corpusName='AppenFY18',
                  versionInfo='1.0',
                  source='official',
                  createdBy=superusers[0]
                )
                _xe_meta = _xe_meta[0]

            else:
                _xe_meta = _xe_meta.first()

        _msg = 'Processed Market/Metadata instances'
        self.stdout.write(_msg)

        # Create CampaignTeam instance
        _cteam = CampaignTeam.objects.get_or_create(
          teamName=CAMPAIGN_NAME,
          owner=superusers[0],
          requiredAnnotations=100 * TASKS * REDUNDANCY,
          requiredHours=(TASKS * REDUNDANCY) / 2,
          createdBy=superusers[0]
        )
        _cteam[0].members.add(superusers[0])
        _cteam[0].save()
        campaign_team_object = _cteam[0]

        _msg = 'Processed CampaignTeam instance'
        self.stdout.write(_msg)

        # Create User accounts
        for code in X_LANGUAGES:
            # EX
            for user_id in range(ANNOTATORS):
                username = '{0}{1}{2:02d}{3:02d}'.format(
                  'eng', code, CAMPAIGN_NO, user_id+1
                )

                hasher = md5()
                hasher.update(username.encode('utf8'))
                hasher.update(CAMPAIGN_KEY.encode('utf8'))
                secret = hasher.hexdigest()[:8]

                if not User.objects.filter(username=username).exists():
                    new_user = User.objects.create_user(
                      username=username, password=secret
                    )
                    new_user.save()

                print(username, secret)

            # XE
            for user_id in range(ANNOTATORS):
                username = '{0}{1}{2:02d}{3:02d}'.format(
                  code, 'eng', CAMPAIGN_NO, user_id+1
                )

                hasher = md5()
                hasher.update(username.encode('utf8'))
                hasher.update(CAMPAIGN_KEY.encode('utf8'))
                secret = hasher.hexdigest()[:8]

                if not User.objects.filter(username=username).exists():
                    new_user = User.objects.create_user(
                      username=username, password=secret
                    )
                    new_user.save()

                print(username, secret)

        _msg = 'Processed User instances'
        self.stdout.write(_msg)

        # Add user instances as CampaignTeam members
        for code in X_LANGUAGES:
            # EX
            for user_id in range(ANNOTATORS):
                username = '{0}{1}{2:02d}{3:02d}'.format(
                  'eng', code, CAMPAIGN_NO, user_id+1
                )

                user_object = User.objects.get(username=username)
                if user_object not in campaign_team_object.members.all():
                    print('{0} --> {1}'.format(
                      campaign_team_object.teamName, user_object.username
                    ))
                    campaign_team_object.members.add(user_object)

            # XE
            for user_id in range(ANNOTATORS):
                username = '{0}{1}{2:02d}{3:02d}'.format(
                  code, 'eng', CAMPAIGN_NO, user_id+1
                )

                user_object = User.objects.get(username=username)
                if user_object not in campaign_team_object.members.all():
                    print('{0} --> {1}'.format(
                      campaign_team_object.teamName, user_object.username
                    ))
                    campaign_team_object.members.add(user_object)

        _msg = 'Processed CampaignTeam members'
        self.stdout.write(_msg)

        return
        

        c = Campaign.objects.filter(campaignName='OfflineEval201710')
        if c.exists():
            c = c[0]
            xe_group = Group.objects.get(name='eng')
            languages = ('ara', 'deu', 'fra', 'ita', 'por', 'rus', 'spa', 'zho')
            for code in languages:
                for i in range(6):
                    username = '{0}{1}{2:02}{3:02}'.format(
                      code, 'eng', campaign_no, i+1
                    )
                    hasher = md5()
                    hasher.update(username.encode('utf8'))
                    hasher.update(campaign_key.encode('utf8'))
                    secret = hasher.hexdigest()[:8]
                    print(username, secret)

                    if not User.objects.filter(username=username).exists():
                        new_user = User.objects.create_user(
                          username=username, password=secret
                        )
                        new_user.save()
                        new_user.groups.add(xe_group)

                ex_group = Group.objects.get(name=code)
                for i in range(6):
                    username = '{0}{1}{2:02}{3:02}'.format(
                      'eng', code, campaign_no, i+1
                    )
                    hasher = md5()
                    hasher.update(username.encode('utf8'))
                    hasher.update(campaign_key.encode('utf8'))
                    secret = hasher.hexdigest()[:8]
                    print(username, secret)

                    if not User.objects.filter(username=username).exists():
                        new_user = User.objects.create_user(
                          username=username, password=secret
                        )
                        new_user.save()
                        new_user.groups.add(ex_group)

            from EvalData.models import DirectAssessmentTask, WorkAgenda
            from collections import defaultdict
            tasks = DirectAssessmentTask.objects.filter(
              campaign=c, activated=True
            )
            tasks_for_market = defaultdict(list)
            users_for_market = defaultdict(list)
            for task in tasks.order_by('id'):
                market = '{0}{1:02}'.format(
                  task.marketName().replace('_', '')[:6],
                  campaign_no
                )
                tasks_for_market[market].append(task)

            for key in tasks_for_market:
                users = User.objects.filter(
                  username__startswith=key
                )

                for user in users.order_by('id'):
                    users_for_market[key].append(user)

                _tasks = []
                for t in tasks_for_market[key]:
                    _tasks.extend([t, t, t])

                _users = users_for_market[key] * 2

                for u, t in zip(_users, _tasks):
                    print(u, '-->', t.id)

                    a = WorkAgenda.objects.filter(
                      user=u, campaign=c
                    )

                    if not a.exists():
                        a = WorkAgenda.objects.create(
                          user=u, campaign=c
                        )
                    else:
                        a = a[0]

                    if t not in a.completedTasks.all():
                        a.openTasks.add(t)

try:
    import fortnitepy
    import sys
    from os import system, name
    import json
    import os
    import crayons
    from fortnitepy.ext import commands
    import datetime
    import BenBotAsync
    from typing import Tuple, Any, Union
    import asyncio
    import functools
    import time
    import aiohttp
    import random
except ModuleNotFoundError as e:
    print(e)
    print(f"Failed to import 1 or more modules. To fix this run 'packages.bat'. \n"
          "If running 'packages.bat' doesn't fix the issue, \n"
          "please join the discord server, and ask for help: https://discord.gg/5U2qNkU")
    exit()
    

def clear():
    if name == 'nt':
        _ = system('cls')
        terminal = 'command prompt'
    else:
        _ = system('clear')
        terminal = 'terminal'
    pass

print(crayons.red(f'loading...'))
time.sleep(5)

def time():
    return datetime.datetime.now().strftime('%H:%M:%S')

def get_device_auth_details():
    if os.path.isfile('device_auths.json'):
        with open('device_auths.json', 'r') as fp:
            return json.load(fp)
    return {}

def store_device_auth_details(email, details):
    existing = get_device_auth_details()
    existing[email] = details

    with open('device_auths.json', 'w') as fp:
        json.dump(existing, fp)

async def event_device_auth_generate(details, email):
    store_device_auth_details(email, details)

with open('config.json', encoding="utf8") as f:
    data = json.load(f)

device_auth_details = get_device_auth_details().get(data['email'], {})
client = commands.Bot(
    command_prefix=data['prefix'],
    auth=fortnitepy.AdvancedAuth(
        email=data['email'],
        password=data['password'],
        prompt_exchange_code=False,
        delete_existing_device_auths=True,
        **device_auth_details
    ),
    status=data['status'],
    platform=fortnitepy.Platform(data['platform'])
)


async def set_and_update_member_prop(schema_key: str, new_value: Any) -> None:
    prop = {schema_key: client.party.me.meta.set_prop(schema_key, new_value)}

    await client.party.me.patch(updated=prop)

async def set_and_update_party_prop(schema_key: str, new_value: Any) -> None:
    prop = {schema_key: client.party.me.meta.set_prop(schema_key, new_value)}

    await client.party.patch(updated=prop)
    
if data['debug']:
    logger = logging.getLogger('fortnitepy.http')
    logger.setLevel(level=logging.DEBUG)
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter('\u001b[36m %(asctime)s:%(levelname)s:%(name)s: %(message)s \u001b[0m'))
    logger.addHandler(handler)

    logger = logging.getLogger('fortnitepy.xmpp')
    logger.setLevel(level=logging.DEBUG)
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter('\u001b[35m %(asctime)s:%(levelname)s:%(name)s: %(message)s \u001b[0m'))
    logger.addHandler(handler)

device_auth_details = get_device_auth_details().get(data['email'], {})
client = commands.Bot(
    command_prefix='!',
    auth=fortnitepy.AdvancedAuth(
        email=data['email'],
        password=data['password'],
        prompt_authorization_code=True,
        delete_existing_device_auths=True,
        **device_auth_details
    ),
    status=data['status'],
    platform=fortnitepy.Platform(data['platform'])
)


@client.event
async def event_device_auth_generate(details: dict, email: str) -> None:
    store_device_auth_details(email, details)

#client ready
clear()
@client.event
async def event_ready():
    member = client.party.me

    await member.edit_and_keep(
        functools.partial(
            fortnitepy.ClientPartyMember.set_outfit,
            asset=data['cid']
        ),
        functools.partial(
            fortnitepy.ClientPartyMember.set_backpack,
            asset=data['bid']
        ),
        functools.partial(
            fortnitepy.ClientPartyMember.set_banner,
            icon=data['banner'],
            color=data['banner_colour'],
            season_level=data['level']
        ),
        functools.partial(
            fortnitepy.ClientPartyMember.set_battlepass_info,
            has_purchased=True,
            level=data['bp_tier']
        )
    )
    
    print(f'                                                                                 ')
    print(crayons.magenta(f'███████╗██╗      █████╗ ██████╗       ██████╗  █████╗ ████████╗'))
    print(crayons.magenta(f'██╔════╝██║     ██╔══██╗██╔══██╗      ██╔══██╗██╔══██╗╚══██╔══╝'))
    print(crayons.magenta(f'█████╗  ██║     ██║  ██║██████╔╝█████╗██████╦╝██║  ██║   ██║   '))
    print(crayons.magenta(f'██╔══╝  ██║     ██║  ██║██╔═══╝ ╚════╝██╔══██╗██║  ██║   ██║   '))
    print(crayons.magenta(f'██║     ███████╗╚█████╔╝██║           ██████╦╝╚█████╔╝   ██║   '))
    print(crayons.magenta(f'╚═╝     ╚══════╝ ╚════╝ ╚═╝           ╚═════╝  ╚════╝    ╚═╝   '))
    print(crayons.red(f'---------------------------------------------------------------------'))
    print(crayons.magenta(f'[FLOP BOT] [{time()}] massive shout out to oli for inspiring me'))
    print(crayons.magenta(f'[FLOP BOT] [{time()}] Discord server: https://discord.gg/7WrH6r3 '))
    print(crayons.magenta(f'[FLOP BOT] [{time()}] For support, questions, etc'))
    print(crayons.cyan(f'[FLOP BOT] [{time()}] This bot is in progress, if  any issue occurs'))
    print(crayons.cyan(f'[FLOP BOT] [{time()}] Please report to the discord ASAP')) 
    print(crayons.red(f'---------------------------------------------------------------------'))
    print(crayons.green(f'[FLOP BOT] [{time()}] Client ready as {client.user.display_name}'))
    print(crayons.red(f'---------------------------------------------------------------------'))

@client.event
async def event_friend_request(request: fortnitepy.PendingFriend) -> None:
  print(f'[FLOP BOT] [{time()}] Received friend request from {request.display_name}')
  
  if data['friend_accept']:
    await request.accept()
    print(f'[FLOP BOT] [{time()}] Accepted friend request from {request.display_name}')
  else:
    await request.decline()
    print(f'[FLOP BOT] [{time()}] Declined friend request from {request.display_name}')
    

# @client.event
# async def event_friend_message(message):
#     print('Received message from {0.author.display_name} | Content: "{0.content}"'.format(message))
#     await message.reply('Could not find command "{0.content"')


@client.event
async def event_party_invite(invite: fortnitepy.ReceivedPartyInvitation):
    await invite.accept()
    print(f'[FLOP BOT] [{time()}] Accepted party invite from {invite.sender.display_name}.')


async def set_vtid(variant_token: str) -> Tuple[str, str, int]:
    async with aiohttp.ClientSession() as session:
        request = await session.request(
            method='GET',
            url='https://benbotfn.tk/api/v1/assetProperties',
            params={
                'path': 'FortniteGame/Content/Athena/'
                        f'Items/CosmeticVariantTokens/{variant_token}.uasset'
            }) # Helo

        response = await request.json()

    file_location = response['export_properties'][0]

    skin_cid = file_location['cosmetic_item']
    variant_channel_tag = file_location['VariantChanelTag']['TagName']
    variant_name_tag = file_location['VariantNameTag']['TagName']

    variant_type = variant_channel_tag.split(
        'Cosmetics.Variant.Channel.'
    )[1].split('.')[0]

    variant_int = int("".join(filter(
        lambda x: x.isnumeric(), variant_name_tag
    )))
    await session.close()
    return skin_cid, variant_type if variant_type != 'ClothingColor' else 'clothing_color', variant_int

@client.event
async def event_party_member_join(member) -> None:
    await client.party.me.set_emote(
        asset=data['eid']
    )
    if client.user.display_name != member.display_name:
        print(f"  [Flop Bot] [{time()}] {member.display_name} has joined the lobby.")

#works
@client.command()
async def skin(ctx: fortnitepy.ext.commands.Context, *, content: str):
    try:
        cosmetic = await BenBotAsync.get_cosmetic(
            lang="en",
            searchLang="en",
            matchMethod="contains",
            name=content,
            backendType="AthenaCharacter"
        )

        await ctx.send(f'Skin set to {cosmetic.id}.')
        print(f'[FLOP BOT] [{time()}] Set skin to: {cosmetic.id}')
        
        await client.party.me.set_outfit(asset=cosmetic.id)

    except BenBotAsync.exceptions.NotFound:
      
        await ctx.send(f"Failed to find a skin with the name: {content}.")
    print(crayons.red(f'[FLOP BOT] [{time()}] Failed to find a skin with the name: {content}.'))

       
#pass for now
@commands.dm_only()
@client.command()
async def unfriend(ctx: fortnitepy.ext.commands.Context, *, epic_username: str):
  
    user = await client.fetch_profile(epic_username)

    if user is not None:
        await client.remove_or_decline_friend(user.id)
        await ctx.send(f'Unfriended {user.display_name}.')
        print(f'[FLOP BOT] [{time()}] Unfriended {user.display_name}.')
    else:
        await ctx.send(f'Failed to unfriend a user with the name: {epic_username}.')
        print(crayons.red(f"[FLOP BOT] [{time()}] [ERROR] Failed to find a user with the name {epic_username}."))

#works
@client.command()
async def season(ctx: fortnitepy.ext.commands.Context, season_number: str) -> None:

    if season_number == '2':
        s1 = "Black Knight"
        seasons = str("CID_035_Athena_Commando_M_Medieval")

    elif season_number == '3':
        s1 = "Reaper"
        seasons = str("CID_084_Athena_Commando_M_Assassin")

    elif season_number == '4':
        s1 = "Omega"
        seasons = str("CID_116_Athena_Commando_M_CarbideBlack")

    elif season_number == '5':
        s1 = "Ragnarok"
        seasons = str("CID_165_Athena_Commando_M_DarkViking")

    elif season_number == '6':
        s1 = "Dire"
        seasons = str("CID_230_Athena_Commando_M_Werewolf")

    elif season_number == '7':
        s1 = "Ice King"
        seasons = str("CID_288_Athena_Commando_M_IceKing")

    elif season_number == '8':
        s1 = "Luxe"
        seasons = str("CID_352_Athena_Commando_F_Shiny")

    elif season_number == '9':
        s1 = "Vendetta"
        seasons = str("CID_407_Athena_Commando_M_BattleSuit")

    elif season_number == '10':
        s1 = "Ultima Knight"
        seasons = str("CID_484_Athena_Commando_M_KnightRemix")

    elif season_number == '11':
        s1 = "Fusion"
        seasons = str("CID_572_Athena_Commando_M_Viper")

    elif season_number == '12':
        s1 = "Midas"
        seasons = str("CID_694_Athena_Commando_M_CatBurglar")
    
    elif season_number == '13':
        s1 = "Eternal Knight"
        seasons = str("CID_767_Athena_Commando_F_Blackknight")

    else:
        seasons = str("CID_221_Athena_Commando_M_Clown")

        await client.party.me.set_emote(
        asset='EID_FacePalm'
    )

    await client.party.me.set_outfit(
        asset=seasons,
        variants=client.party.me.create_variants(profile_banner='ProfileBanner')
    )

    await ctx.send(f"Skin set to season {season_number}'s tier 100 skin")
    print(f"[FLOP BOT] [{time()}] Skin set to season {season_number}'s tier 100 skin")


#chapter command
#works
@client.command()
async def chapter(ctx: fortnitepy.ext.commands.Context, chapter_number: str) -> None:
    if chapter_number == '1':
        c1 = "Black Knight"
        chapter = str("CID_035_Athena_Commando_M_Medieval")
    elif chapter_number == '2':
        c1 = "Midas"
        chapter = str("CID_694_Athena_Commando_M_CatBurglar")

    await client.party.me.set_outfit(
        asset=chapter,
        variants=client.party.me.create_variants(profile_banner='ProfileBanner')
    )

    await ctx.send(f'Skin set to {c1} from Chapter {chapter_number}')
    print(f'[FLOP BOT] [{time()}] Skin set to {c1} from Chapter {chapter_number}')


#end of chapter command

#
@client.command()
async def gift(ctx: fortnitepy.ext.commands.context) -> None:
  
    await client.party.me.clear.emote()

    await client.party.me.set_emote(
       asset='eid_nevergonna'
      )

    await ctx.send('you thought kid buy vbucks') #
    print(f'[FLOP BOT] [{time()}] Some dude tryin to get gifted')

#works
@client.command()
async def uninstall( ctx: fortnitepy.ext.commands.Context) -> None:
      
    await client.party.me.clear_emote()

    await client.party.me.set_emote(asset='EID_nottoday')

    await ctx.send('If u thought this was gonna work u deserve to be hit with bred stick!!!')
    print(f'[FLOP BOT] [{time()}] Successfully uninstalled Fortnite.')

#works
@commands.dm_only()
@client.command()
async def leave(ctx: fortnitepy.ext.commands.Context) -> None:
    await client.party.me.set_emote('EID_Wave')
    await asyncio.sleep(2)
    await client.party.me.leave()
    await ctx.send('Bye!')

    print(f'[FLOP BOT] [{time()}] Left the party as I was requested.')


#works
@client.command()
async def backpack(ctx: fortnitepy.ext.commands.Context, *, content: str) -> None:
    try:
        cosmetic = await BenBotAsync.get_cosmetic(
            lang="en",
            searchLang="en",
            matchMethod="contains",
            name=content,
            backendType="AthenaBackpack"
        )

        await ctx.send(f'Set backpack to {content} ({cosmetic.id}).')
        print(f"[FLOP BOT] [{time()}] Backpack set to: {content} ({cosmetic.id}).")
        await client.party.me.set_backpack(asset=cosmetic.id)

    except BenBotAsync.exceptions.NotFound:
        await ctx.send(f"Can not find an backpack with name: {content}.")
        print(f"[FLOP BOT] [{time()}] Can not find an backbling with name: {content}.")

#works
@client.command()
async def level(ctx: fortnitepy.ext.commands.Context, banner_level: int) -> None:
  await client.party.me.set_banner(
    season_level=banner_level
  )
  
  await ctx.send(f'Level set to {banner_level}')
  print(f'[FLOP BOT] [{time()}] Level set to {banner_level}')
 
  
#works
@client.command()
async def bp(ctx: fortnitepy.ext.commands.Context, tier: int) -> None:
   await client.party.me.set_battlepass_info(
      has_purchased=True,
      level=tier
  )
  
   await ctx.send(f'Battlepass tier set to {tier}')
   print(f'[FLOP BOT] [{time()}] Battlepass tier set to {tier}')
    
#doesnt work
@client.command()
async def copy(ctx: fortnitepy.ext.commands.Context, *, epic_username: str = None) -> None:
    if epic_username is None:
        member = client.party.members.get(ctx.author.id)
    else:
        user = await client.fetch_profile(epic_username)
        member = client.party.members.get(user.id)

    await client.party.me.edit(
        functools.partial(
            fortnitepy.ClientPartyMember.set_outfit,
            asset=member.outfit,
            variants=member.outfit_variants
        ),
        functools.partial(
            fortnitepy.ClientPartyMember.set_backpack,
            asset=member.backpack,
            variants=member.backpack_variants
        ),
        functools.partial(
            fortnitepy.ClientPartyMember.set_pickaxe,
            asset=member.pickaxe,
            variants=member.pickaxe_variants
        ),
        functools.partial(
            fortnitepy.ClientPartyMember.set_banner,
            icon=member.banner[0],
            color=member.banner[1],
            season_level=member.banner[2]
        ),
        functools.partial(
            fortnitepy.ClientPartyMember.set_battlepass_info,
            has_purchased=True,
            level=member.battlepass_info[1]
        )
    )

    await client.party.me.set_emote(asset=member.emote)
    await ctx.send(f'Copied the loadout of {member.display_name}.')
#works     
@client.command()
async def hologram(ctx: fortnitepy.ext.commands.Context) -> None:
    await client.party.me.set_outfit(asset='CID_VIP_Athena_Commando_M_GalileoGondola_SG')
    

    await ctx.send('Skin set to Hologram!')
    print(f'[FLOP BOT] [{time()}] Skin set to hologram.')


@client.command()
async def emote(ctx: fortnitepy.ext.commands.Context, *, content: str) -> None:
    try:
        cosmetic = await BenBotAsync.get_cosmetic(
            lang="en",
            searchLang="en",
            matchMethod="contains",
            name=content,
            backendType="AthenaDance"
        )

        await ctx.send(f'Emote set to {cosmetic.id}.')
        print(f"[FLOP bot] [{time()}] Set emote to: {cosmetic.id}.")
        await client.party.me.clear_emote()
        await client.party.me.set_emote(asset=cosmetic.id)

    except BenBotAsync.exceptions.NotFound:
        await ctx.send(f"Failed to find an emote with the name: {content}.")
        print(f"[FLOP BOT] [{time()}] Failed to find an emote with the name: {content}.")

        
@client.command()
async def stop(ctx: fortnitepy.ext.commands.Context) -> None:
    await client.party.me.clear_emote()
    await ctx.send('Stopped emoting')
    print(f'[FLOP BOT] [{time()}] Stopped emoting')
   

@client.command()
async def matchmakingcode(ctx: fortnitepy.ext.commands.Context, *, custom_matchmaking_key: str) -> None:
    await client.party.set_custom_key(key=custom_matchmaking_key)

    await ctx.send(f'Custom matchmaking code set to: {custom_matchmaking_key}')
    print(crayons.red(f'[FLOP BOT] [{time()}] matchmaking code set to {custom_matchmaking_key}'))
    
   
@commands.dm_only()
@client.command()
async def match(ctx: fortnitepy.ext.commands.Context, players: Union[str, int] = 0, match_time: int = 0) -> None:
    if players == 'progressive':
        match_time = datetime.datetime.utcnow()

        await client.party.me.set_in_match(
            players_left=100,
            started_at=match_time
        )

        while (100 >= client.party.me.match_players_left > 0
               and client.party.me.in_match()):

            await client.party.me.set_in_match(
                players_left=client.party.me.match_players_left - py_random.randint(3, 6),
                started_at=match_time
            )

            await asyncio.sleep(py_random.randint(45, 65))

    else:
        await client.party.me.set_in_match(
            players_left=int(players),
            started_at=datetime.datetime.utcnow() - datetime.timedelta(minutes=match_time)
        )

        await ctx.send(f'Set state to in-game in a match with {players} players.'
                       '\nUse the command: !lobby to revert back to normal.')

@commands.dm_only()
@client.command()
async def lobby(ctx: fortnitepy.ext.commands.Context) -> None:
    if client.default_party_member_config.cls == fortnitepy.JustChattingClientPartyMember:
        client.default_party_member_config.cls = fortnitepy.ClientPartyMember

        party_id = client.party.id
        await client.party.me.leave()

        await ctx.send('Removed state of Just Chattin\'. Now attempting to rejoin party.')

        try:
            await client.join_to_party(party_id)
        except fortnitepy.errors.Forbidden:
            await ctx.send('Failed to join back as party is set to private.')
        except fortnitepy.errors.NotFound:
            await ctx.send('Party not found, are you sure Fortnite is open?')

    await client.party.me.clear_in_match()

    await ctx.send('Set state to the pre-game lobby.')

@client.command()
async def pickaxe(ctx: fortnitepy.ext.commands.Context, *, content: str) -> None:
  try:
    cosmetic = await BenBotAsync.get_cosmetic(
       lang="en",
       searchLang="en",
       matchMethod="contains",
       name=content,
       backendType="AthenaPickaxe"
    )
    
    
    await ctx.send(f'Set pickaxe to: {content} ({cosmetic.id})')
    print(f'[FLOP BOT] [{time()}] Pickaxe set to: {content} ({cosmetic.id})')
    await client.party.me.set_pickaxe(asset=cosmetic.id)
    
  except BenBotAsync.exceptions.NotFound:
    await ctx.send(f'Failed to find a pickaxe with name: {content}')
    print(f'[FLOP BOT] [{time()}] [ERROR] Failed to find a pickaxe with name: {content}')
    

@client.command()
async def point(ctx: fortnitepy.ext.commands.Context, *, content: str = None) -> None:
    if content is None:
        await client.party.me.set_emote(asset='EID_IceKing')
        await ctx.send(f'Point it Out played.')
    elif 'pickaxe_id' in content.lower():
        await client.party.me.set_pickaxe(asset=content)
        await client.party.me.set_emote(asset='EID_IceKing')
        await ctx.send(f'Pickaxe set to {content} & Point it Out played.')
    else:
        try:
            cosmetic = await BenBotAsync.get_cosmetic(
                lang="en",
                searchLang="en",
                matchMethod="contains",
                name=content,
                backendType="AthenaPickaxe"
            )

            await client.party.me.set_pickaxe(asset=cosmetic.id)
            await client.party.me.clear_emote()
            await client.party.me.set_emote(asset='EID_IceKing')
            await ctx.send(f'Pickaxe set to {content} & Point it Out played.')
        except BenBotAsync.exceptions.NotFound:
            await ctx.send(f"Failed to find a pickaxe with the name: {content}")
            
@client.command()
async def eid(ctx: fortnitepy.ext.commands.Context, emote_id: str) -> None:
    await client.party.me.clear_emote()
    await client.party.me.set_emote(
        asset=emote_id
    )

    await ctx.send(f'Emote set to {emote_id}!')
 
@commands.dm_only()
@client.command()
async def hide(ctx: fortnitepy.ext.commands.Context, party_member: Union[str, None] = None) -> None:
    if client.party.me.leader:
        if party_member is not None:
            user = await client.fetch_profile(party_member)
            member = client.party.members.get(user.id)

            if member is not None:
                raw_squad_assignments = client.party.meta.get_prop('Default:RawSquadAssignments_j')["RawSquadAssignments"]

                for player in raw_squad_assignments:
                    if player['memberId'] == member.id:
                        raw_squad_assignments.remove(player)

                await set_and_update_party_prop(
                    'Default:RawSquadAssignments_j', {
                        'RawSquadAssignments': raw_squad_assignments
                    }
                )
            else:
                await ctx.send(f'Failed to find user with the name: {party_member}.')
                print(crayons.red(f"[FLOP BOT] [{time()}] [ERROR] "
                                  f"Failed to find user with the name: {party_member}."))
        else:
            await set_and_update_party_prop(
                'Default:RawSquadAssignments_j', {
                    'RawSquadAssignments': [{'memberId': client.user.id, 'absoluteMemberIdx': 1}]
                }
            )

            await ctx.send('Hid everyone in the party. Use !unhide if you want to unhide everyone.')
            print(f'[FLOP BOT] [{time()}] Hid everyone in the party.')
    else:
        await ctx.send("Failed to hide everyone, as I'm not party leader")
        print(crayons.red(f"[FLOP BOT] [{time()}] [ERROR] "
                          "Failed to hide everyone as I don't have the required permissions."))
        
        
@commands.dm_only()
@client.command(aliases=['unhide'])
async def promote(ctx: fortnitepy.ext.commands.Context, *, epic_username: str = None) -> None:
    if epic_username is None:
        user = await client.fetch_profile(ctx.author.display_name)
        member = client.party.members.get(user.id)
    else:
        user = await client.fetch_profile(epic_username)
        member = client.party.members.get(user.id)

    if member is None:
        await ctx.send("Failed to find that user, are you sure they're in the party?")
    else:
        try:
            await member.promote()
            await ctx.send(f"Promoted user: {member.display_name}.")
            print(f"[Flop Bot] [{time()}] Promoted user: {member.display_name}")
        except fortnitepy.errors.Forbidden:
            await ctx.send(f"Failed topromote {member.display_name}, as I'm not party leader.")
            print(crayons.red(f"[Flop Bot] [{time()}] [ERROR] "
                              "Failed to kick member as I don't have the required permissions."))
      
@client.command()
async def purpleskull(ctx: fortnitepy.ext.commands.Context) -> None:
    skin_variants = client.party.me.create_variants(
        clothing_color=1
    )

    await client.party.me.set_outfit(
        asset='CID_030_Athena_Commando_M_Halloween',
        variants=skin_variants
    )

    await ctx.send('Skin set to Purple Skull Trooper!')
    print(f"[FLOP BOT] [{time()}] Skin set to Purple Skull Trooper.")


@client.command()
async def pinkghoul(ctx: fortnitepy.ext.commands.Context) -> None:
    skin_variants = client.party.me.create_variants(
        material=3
    )

    await client.party.me.set_outfit(
        asset='CID_029_Athena_Commando_F_Halloween',
        variants=skin_variants
    )

    await ctx.send('Skin set to Pink Ghoul Trooper!')
    print(f"[FLOP BOT] [{time()}] Skin set to Pink Ghoul Trooper.")


@client.command()
async def purpleportal(ctx: fortnitepy.ext.commands.Context) -> None:
    skin_variants = client.party.me.create_variants(
        item='AthenaBackpack',
        particle_config='Particle',
        particle=1
    )

    await client.party.me.set_backpack(
        asset='BID_105_GhostPortal',
        variants=skin_variants
    )

    await ctx.send('Backpack set to Purple Ghost Portal!')
    print(f"[FLOP BOT] [{time()}] Backpack set to Purple Ghost Portal.")


    
@commands.dm_only()
@client.command()
async def cid(ctx: fortnitepy.ext.commands.Context, character_id: str) -> None:
    await client.party.me.set_outfit(
        asset=character_id,
        variants=client.party.me.create_variants(profile_banner='ProfileBanner')
    )

    await ctx.send(f'Skin set to {character_id}')
    print(f'[Flop Bot] [{time()}] Skin set to {character_id}')

    
@client.command()
async def CID(ctx: fortnitepy.ext.commands.Context, skin_id: str) -> None:
  await client.party.me.set_outfit(
  asset=skin_id,
  variants=client.party.me.create_variants(profile_banner='ProfileBanner')
  )
  
  await ctx.send(f'Skin set to {skin_id}')
  print(f'[Flop Bot] [{time()}] Skin set to {skin_id}')
              
@client.command()
async def pet(ctx: fortnitepy.ext.commands.Context, *, content: str) -> None:
    try:
        cosmetic = await BenBotAsync.get_cosmetic(
            lang="en",
            searchLang="en",
            matchMethod="contains",
            name=content,
            backendType="AthenaPet"
        )

        await ctx.send(f'Pet set to {cosmetic.id}.')
        print(f"[FLOP BOT] [{time()}] Set pet to: {cosmetic.id}.")
        await client.party.me.set_pet(asset=cosmetic.id)

    except BenBotAsync.exceptions.NotFound:
        await ctx.send(f"Failed to find a pet with the name: {content}.")
        print(f"[FLOP BOT] [{time()}] Failed to find a pet with the name: {content}.")

@client.command()
async def help(ctx: fortnitepy.ext.commands.Context, str) -> None:
    await ctx.send(f"if any problems do occur please report to the discord ASAP [commands in discord].")
    print(f"  [FLOP BOT] [{time()}] if any problems do occur please report to the discord ASAP [commands in discord].")            

@commands.dm_only()
@client.command()
async def join(ctx: fortnitepy.ext.commands.Context, *, epic_username: str = None) -> None:
    if epic_username is None:
        epic_friend = client.get_friend(ctx.author.id)
    else:
        user = await client.fetch_profile(epic_username)

        if user is not None:
            epic_friend = client.get_friend(user.id)
        else:
            epic_friend = None
            await ctx.send(f'Failed to find user with the name: {epic_username}.')

    if isinstance(epic_friend, fortnitepy.Friend):
        try:
            await epic_friend.join_party()
            await ctx.send(f'Joined the party of {epic_friend.display_name}.')
        except fortnitepy.errors.Forbidden:
            await ctx.send('Failed to join party since it is private.')
        except fortnitepy.errors.PartyError:
            await ctx.send('Party not found, are you sure Fortnite is open?')
    else:
        await ctx.send('Cannot join party as the friend is not found.')

# members = []
# 
# @commands.dm_only()
# @client.command()
# async def kickall(ctx: fortnitepy.ext.commands.context, *, cache: bool=False List[fortnitepy.user.User]:
#     user = await client.fetch_profiles(users)
#     member = client.party.members.get(user.id)
#     
#     for members in members:
#         member.kick()

#     if member is None:
#         await ctx.send("Failed to find that user, are you sure they're in the party?")
#     else:
#         try:
#             await member.kick()
#             await ctx.send(f"Kicked user: {member.display_name}.")
#             print(f"[PartyBot] [{time()}] Kicked user: {member.display_name}")
#         except fortnitepy.errors.Forbidden:
#             await ctx.send(f"Failed to kick {member.display_name}, as I'm not party leader.")
#             print(crayons.red(f"[PartyBot] [{time()}] [ERROR] "
#                               "Failed to kick member as I don't have the required permissions."))


@commands.dm_only()
@client.command()
async def ready(ctx: fortnitepy.ext.commands.Context) -> None:
    await client.party.me.set_ready(fortnitepy.ReadyState.READY)
    await ctx.send('Ready!')
    print(crayons.green(f"[FLOP BOT] [{time()}] bot ready.")) 

@commands.dm_only()
@client.command(aliases=['sitin'])
async def unready(ctx: fortnitepy.ext.commands.Context) -> None:
    await client.party.me.set_ready(fortnitepy.ReadyState.NOT_READY)
    await ctx.send('Unready!')
    print(crayons.green(f"[FLOP BOT] [{time()}] bot unready.")) 



@commands.dm_only()
@client.command()
async def goldenpeely(ctx: fortnitepy.ext.commands.Context) -> None:
    await client.party.me.set_outfit(
        asset='CID_701_Athena_Commando_M_BananaAgent',
        variants=client.party.me.create_variants(progressive=4),
        enlightenment=(2, 350)
    )

    await ctx.send(f'Skin set to Golden Peely.')
    print(f"[FLOP BOT] [{time()}] golden peely.")

@commands.dm_only()
@client.command()
async def kick(ctx: fortnitepy.ext.commands.Context, *, epic_username: str) -> None:
    user = await client.fetch_profile(epic_username)
    member = client.party.members.get(user.id)

    if member is None:
        await ctx.send("Failed to find that user, are you sure they're in the party?")
    else:
        try:
            await member.kick()
            await ctx.send(f"Kicked user: {member.display_name}.")
            print(f"[FLOP BOT] [{time()}] Kicked user: {member.display_name}")
        except fortnitepy.errors.Forbidden:
            await ctx.send(f"Failed to kick {member.display_name}, as I'm not party leader.")
            print(crayons.red(f"[FLOP BOT] [{time()}] [ERROR] "
                              "Failed to kick member as I don't have the required permissions."))

@commands.dm_only()
@client.command()
async def default(ctx: fortnitepy.ext.commands.Context) -> None:
    print(crayons.green(f"[FLOP BOT] [{time()}] Set to an OG default.")) 
    default = ['CID_001_Athena_Commando_F_Default', 'CID_002_Athena_Commando_F_Default', 'CID_003_Athena_Commando_F_Default', 'CID_004_Athena_Commando_F_Default', 'CID_005_Athena_Commando_M_Default', 'CID_006_Athena_Commando_M_Default', 'CID_007_Athena_Commando_M_Default', 'CID_008_Athena_Commando_M_Default']
    defaulty = random.choice(default)
    await client.party.me.set_outfit(asset=defaulty)

@commands.dm_only()
@client.command()
async def shutdown(ctx: fortnitepy.ext.commands.Context) -> None:
    exit()
    print(f'[FLOP Bot] [{time()}] Shutting down...')


@commands.dm_only()
@client.command()
async def clean(ctx: fortnitepy.ext.commands.Context) -> None:
    await ctx.send('Cleared CMD')
    clear()
    print(crayons.magenta(f'███████╗██╗      █████╗ ██████╗       ██████╗  █████╗ ████████╗'))
    print(crayons.magenta(f'██╔════╝██║     ██╔══██╗██╔══██╗      ██╔══██╗██╔══██╗╚══██╔══╝'))
    print(crayons.magenta(f'█████╗  ██║     ██║  ██║██████╔╝█████╗██████╦╝██║  ██║   ██║   '))
    print(crayons.magenta(f'██╔══╝  ██║     ██║  ██║██╔═══╝ ╚════╝██╔══██╗██║  ██║   ██║   '))
    print(crayons.magenta(f'██║     ███████╗╚█████╔╝██║           ██████╦╝╚█████╔╝   ██║   '))
    print(crayons.magenta(f'╚═╝     ╚══════╝ ╚════╝ ╚═╝           ╚═════╝  ╚════╝    ╚═╝   '))
    print(crayons.red(f'---------------------------------------------------------------------'))
    print(crayons.magenta(f'[FLOP BOT] [{time()}] massive shout out to oli for inspiring me'))
    print(crayons.magenta(f'[FLOP BOT] [{time()}] Discord server: https://discord.gg/7WrH6r3 '))
    print(crayons.magenta(f'[FLOP BOT] [{time()}] For support, questions, etc'))
    print(crayons.cyan(f'[FLOP BOT] [{time()}] This bot is in progress, if  any issue occurs'))
    print(crayons.cyan(f'[FLOP BOT] [{time()}] Please report to the discord ASAP')) 
    print(crayons.red(f'---------------------------------------------------------------------'))
    print(crayons.green(f'[FLOP BOT] [{time()}] Client ready as {client.user.display_name}'))
    print(crayons.red(f'---------------------------------------------------------------------'))

@client.command()
async def shop(ctx: fortnitepy.ext.commands.Context) -> None:
    store = await client.fetch_item_shop()


    await ctx.send(f"Equipping all skins in today's item shop.")
    print(f"[FLOP BOT] [{time()}] Equipping all skins in today's item shop.")

    for item in store.featured_items + store.daily_items:
        for grant in item.grants:
            if grant['type'] == 'AthenaCharacter':
                await client.party.me.set_outfit(
                    asset=grant['asset']
                )

                await ctx.send(f"Skin set to {item.display_names[0]} Worth {item.price} Vbucks!!!")
                print(f"[FLOP BOT] [{time()}] Skin set to: {item.display_names[0]} Worth {item.price} Vbucks!!!")

                await asyncio.sleep(3)

    await ctx.send(f'Finished equipping all skins in the item shop. This Item Shop Expires in  {store.expires_at}')
    print(f'[FLOP BOT] [{time()}] Finished equipping all skins in the item shop. This Item Shop Expires in  {store.expires_at}')

@commands.dm_only()
@client.command()
async def new(ctx: fortnitepy.ext.commands.Context) -> None:
    async with aiohttp.ClientSession() as session:
        request = await session.request(
            method='GET',
            url='https://benbotfn.tk/api/v1/files/added',
        )

        response = await request.json()

    for new_skin in [new_cid for new_cid in response if new_cid.split('/')[-1].lower().startswith('eid_')]:
        await client.party.me.set_emote(
            asset=new_skin.split('/')[-1].split('.uasset')[0]
        )

        await ctx.send(f"Skin set to {new_skin.split('/')[-1].split('.uasset')[0]}!")
        print(f"[FLOP BOT] [{time()}] Skin set to: {new_skin.split('/')[-1].split('.uasset')[0]}!")

        await asyncio.sleep(3)

    await ctx.send(f'Finished equipping all new unencrypted skins.')
    print(f'[FLOP BOT] [{time()}] Finished equipping all new unencrypted skins.')

    for new_emote in [new_eid for new_eid in response if new_eid.split('/')[-1].lower().startswith('eid_')]:
        await client.party.me.set_emote(
            asset=new_skin.split('/')[-1].split('.uasset')[0]
        )

        await ctx.send(f"Emote set to {new_eid.split('/')[-1].split('.uasset')[0]}!")
        print(f"[FLOP BOT] [{time()}] Emote set to: {new_eid.split('/')[-1].split('.uasset')[0]}!")

        await asyncio.sleep(3)

    await ctx.send(f'Finished equipping all new unencrypted skins.')
    print(f'[FLOP BOT] [{time()}] Finished equipping all new unencrypted skins.')


@commands.dm_only()
@client.command()
async def justchattin(ctx: fortnitepy.ext.commands.Context) -> None:
    client.default_party_member_config.cls = fortnitepy.JustChattingClientPartyMember

    party_id = client.party.id
    await client.party.me.leave()

    await ctx.send('Set state to Just Chattin\'. Now attempting to rejoin party.'
                   '\nUse the command: !lobby to revert back to normal.')

    try:
        await client.join_to_party(party_id)
    except fortnitepy.errors.Forbidden:
        await ctx.send('Failed to join back as party is set to private.')
    except fortnitepy.errors.NotFound:
        await ctx.send('Party not found, are you sure Fortnite is open?')

@commands.dm_only()
@client.command()
async def style(ctx: fortnitepy.ext.commands.Context, cosmetic_name: str, variant_type: str, variant_int: str) -> None:
    # cosmetic_types = {
    #     "AthenaCharacter": client.party.me.set_outfit,
    #     "AthenaBackpack": client.party.me.set_backpack,
    #     "AthenaPickaxe": client.party.me.set_pickaxe
    # }

    cosmetic = await BenBotAsync.get_cosmetic(
        lang="en",
        searchLang="en",
        matchMethod="contains",
        name=cosmetic_name,
        backendType="AthenaCharacter"
    )

    cosmetic_variants = client.party.me.create_variants(
        # item=cosmetic.backend_type.value,
        **{variant_type: int(variant_int) if variant_int.isdigit() else variant_int}
    )

    # await cosmetic_types[cosmetic.backend_type.value](
    await client.party.me.set_outfit(
        asset=cosmetic.id,
        variants=cosmetic_variants
    )

    await ctx.send(f'Set variants of {cosmetic.id} to {variant_type} {variant_int}.')
    print(f'[FLOP BOT] [{time()}] Set variants of {cosmetic.id} to {variant_type} {variant_int}.')

@commands.dm_only()
@client.command()
async def variants(ctx: fortnitepy.ext.commands.Context, cosmetic_id: str, variant_type: str, variant_int: str) -> None:
    if 'cid' in cosmetic_id.lower() and 'jersey_color' not in variant_type.lower():
        skin_variants = client.party.me.create_variants(
            **{variant_type: int(variant_int) if variant_int.isdigit() else variant_int}
        )

        await client.party.me.set_outfit(
            asset=cosmetic_id,
            variants=skin_variants
        )

    elif 'cid' in cosmetic_id.lower() and 'jersey_color' in variant_type.lower():
        cosmetic_variants = client.party.me.create_variants(
            pattern=0,
            numeric=69,
            **{variant_type: int(variant_int) if variant_int.isdigit() else variant_int}
        )

        await client.party.me.set_outfit(
            asset=cosmetic_id,
            variants=cosmetic_variants
        )

    elif 'bid' in cosmetic_id.lower():
        cosmetic_variants = client.party.me.create_variants(
            item='AthenaBackpack',
            **{variant_type: int(variant_int) if variant_int.isdigit() else variant_int}
        )

        await client.party.me.set_backpack(
            asset=cosmetic_id,
            variants=cosmetic_variants
        )
    elif 'pickaxe_id' in cosmetic_id.lower():
        cosmetic_variants = client.party.me.create_variants(
            item='AthenaPickaxe',
            **{variant_type: int(variant_int) if variant_int.isdigit() else variant_int}
        )

        await client.party.me.set_pickaxe(
            asset=cosmetic_id,
            variants=cosmetic_variants
        )

    await ctx.send(f'Set variants of {cosmetic_id} to {variant_type} {variant_int}.')
    print(f'[FLOP BOT] [{time()}] Set variants of {cosmetic_id} to {variant_type} {variant_int}.')

@commands.dm_only()
@client.command()
async def set(ctx: fortnitepy.ext.commands.Context, *, content: str) -> None:
    cosmetic_types = {
        "AthenaBackpack": client.party.me.set_backpack,
        "AthenaCharacter": client.party.me.set_outfit,
        "AthenaEmoji": client.party.me.set_emoji,
        "AthenaDance": client.party.me.set_emote
    }

    set_items = await BenBotAsync.get_cosmetics(
        lang="en",
        searchLang="en",
        matchMethod="contains",
        set=content
    )

    await ctx.send(f'Equipping all cosmetics from the {set_items[0].set} set.')
    print(f'[FLOP BOT] [{time()}] Equipping all cosmetics from the {set_items[0].set} set.')

    for cosmetic in set_items:
        if cosmetic.backend_type.value in cosmetic_types:
            await cosmetic_types[cosmetic.backend_type.value](asset=cosmetic.id)

            await ctx.send(f'{cosmetic.short_description} set to {cosmetic.name}!')
            print(f'[FLOP BOT] [{time()}] {cosmetic.short_description} set to {cosmetic.name}.')

            await asyncio.sleep(3)

    await ctx.send(f'Finished equipping all cosmetics from the {set_items[0].set} set.')
    print(f'[FLOP BOT] [{time()}] Fishing equipping  all cosmetics from the {set_items[0].set} set.')   

@commands.dm_only()
@client.command()
async def playlist_id(ctx: fortnitepy.ext.commands.Context, playlist_: str) -> None:
    try:
        await client.party.set_playlist(playlist=playlist_)
        await ctx.send(f'Gamemode set to {playlist_}')
    except fortnitepy.errors.Forbidden:
        await ctx.send(f"Failed to set gamemode to {playlist_}, as I'm not party leader.")
        print(crayons.red(f"[FLOP BOT] [{time()}] [ERROR] "
                          "Failed to set gamemode as I don't have the required permissions."))


@commands.dm_only()
@client.command()
async def playlist(ctx: fortnitepy.ext.commands.Context, *, playlist_name: str) -> None:
    try:
        scuffedapi_playlist_id = await get_playlist(playlist_name)

        if scuffedapi_playlist_id is not None:
            await client.party.set_playlist(playlist=scuffedapi_playlist_id)
            await ctx.send(f'Playlist set to {scuffedapi_playlist_id}.')
            print(f'[FLOP BOT] [{time()}] Playlist set to {scuffedapi_playlist_id}.')

        else:
            await ctx.send(f'Failed to find a playlist with the name: {playlist_name}.')
            print(crayons.red(f"[FLOP BOT] [{time()}] [ERROR] "
                              f"Failed to find a playlist with the name: {playlist_name}."))

    except fortnitepy.errors.Forbidden:
        await ctx.send(f"Failed to set playlist to {playlist_namet}, as I'm not party leader.")
        print(crayons.red(f"[FLOP BOT] [{time()}] [ERROR] "

                          "Failed to set playlist as I don't have the required permissions."))

@commands.dm_only()
@client.command(aliases=['legacypickaxe'])
async def pickaxe_id(ctx: fortnitepy.ext.commands.Context, pickaxe_id_: str) -> None:
    await client.party.me.set_pickaxe(
        asset=pickaxe_id_
    )

    await ctx.send(f'Pickaxe set to {pickaxe_id_}') 
#--- Do Not Change Anything Below ---
client.run()
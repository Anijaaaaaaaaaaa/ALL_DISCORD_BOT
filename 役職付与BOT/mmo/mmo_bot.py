import asyncio
import re
import discord
import aiomysql
import traceback
import getpass
import random
from discord.ext import commands

no = '👎'
ok = '👍'
left = '⏪'
right = '⏩'
counts = 0
admin_id = [304932786286886912, 460208854362357770, 574166391071047694, 294362309558534144, 550248294551650305]
user_list = []


def shuffle(d):
    keys = list(d.keys())
    random.shuffle(keys)
    keys = [(key, d[key]) for key in keys]
    return dict(keys)


def predicate(message, author, l, r, bot):
    def check(reaction, user):
        if reaction.message.id != message.id or user == bot.user or author != user:
            return False
        if l and reaction.emoji == left or r and reaction.emoji == right:
            return True
    return check


def predicate1(message, author, bot):
    def check(reaction, user):
        if reaction.message.id != message.id or user == bot.user or author != user:
            return False
        if reaction.emoji == ok or reaction.emoji == no:
            return True
        return False
    return check


class Bots(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='help', description='このBOTのすべての機能を書いた', hidden=True)
    async def ok(self, ctx):
        help_message = [f"```[&members 役職名] | その役職が誰に付与されているのかを全て表示します\n[&all-role] | 鯖の全ての役職を表示します\n[&self-role] | 自分が付与されてい���役職を表示します\n[&roles] | 超激レア報告用```\n```『#超激レア出現ログ』作ってみてね！```\n`1ページ目/2ページ中`",
                        f"```注意:これらのコマンドは管理者権限がないと操作できません。```\n```[&level lower upper 役職名] | [例: &level 1 10 aaa]\nこれで自分のTAOでのレベルが1~10の時に役職名:『aaa』が自動付与されます。\n[&list] | 今設定されている役職の全てを表示されます\n[&reset] | 設定されている役職の全てをリセットします```\n```『#役職更新ログ』というチャンネルを作成したら色んな人が役職を\n更新した際にそのチャンネルにログが残るようになります。```\n`2ページ目/2ページ目`"]
        index = 0
        while True:
            embed = discord.Embed(title=f"{self.bot.user}の使い方:", description=help_message[index])
            embed.set_thumbnail(url=self.bot.user.avatar_url)
            embed.add_field(name="SERVERの数", value=f"`{len(self.bot.guilds)}`")
            embed.add_field(name="USERの数", value=f"`{len(set(self.bot.get_all_members()))}`")
            embed.add_field(name="言語", value="`discord.py`")
            embed.add_field(name="Latency", value=f"`{self.bot.ws.latency * 1000:.0f}ms`")
            embed.add_field(name="各種リンク", value="[このBOTの招待](<https://discordapp.com/oauth2/authorize?client_id=550248294551650305&permissions=8&scope=bot>) ,[このBOTの公式サーバー](<https://discord.gg/4YB8gXv>)", inline=False)
            embed.set_footer(text=f"制作者:{self.bot.get_user(304932786286886912)} | 編集者: {self.bot.get_user(574166391071047694)}, {self.bot.get_user(204966469593858048)}",)
            msg = await ctx.send(embed=embed)
            ll = index != 0
            r = index != len(help_message) - 1
            if ll:
                await msg.add_reaction(left)
            if r:
                await msg.add_reaction(right)
            try:
                react = await self.bot.wait_for('reaction_add', timeout=20, check=predicate(msg, ctx.message.author, ll, r, self.bot))
                if react[0].emoji == left:
                    index -= 1
                elif react[0].emoji == right:
                    index += 1
                await msg.delete()
            except asyncio.TimeoutError:
                return

    @commands.command(name='members', description='このBOTのすべての機能を書いた', hidden=True)
    async def list_of_role(self, ctx, *, role_name=""):
        try:
            role = discord.utils.get(ctx.message.guild.roles, name=role_name)
            if not role_name:
                msg = discord.Embed(description=f"{ctx.message.author.mention}さん\n役職名はちゃんと入力して下さい！", color=0xC41415)
                return await ctx.send(embed=msg)
            elif not role:
                msg = discord.Embed(description=f"{ctx.message.author.mention}さん\nその名前の役職は存在してないそうですよ？", color=0xC41415)
                return await ctx.send(embed=msg)
            else:
                role_members = [member for member in ctx.message.guild.members if role in member.roles]
                list_role_memebrs = "".join([f"{k+1}人目:『{member.mention}』\n" for member, k in zip(role_members, range(0, len(role_members)))])
                ranking_msgs = ["\n".join(list_role_memebrs.split("\n")[i:i + 50]) for i in range(0, len(role_members), 50)]
                index = 0
                while True:
                    msg = await ctx.send(embed=discord.Embed(title=f"『{role_name}』役職を持っているメンバー！！", description=ranking_msgs[index]))
                    ll = index != 0
                    r = index != len(ranking_msgs) - 1
                    if ll:
                        await msg.add_reaction(left)
                    if r:
                        await msg.add_reaction(right)
                    react = await self.bot.wait_for('reaction_add', timeout=10, check=predicate(msg, ctx.message.author, ll, r, self.bot))
                    if react[0].emoji == left:
                        index -= 1
                    if react[0].emoji == right:
                        index += 1
                    await msg.delete()
        except asyncio.TimeoutError:
            pass

    @commands.command(name='all-role', description='このBOTのすべての機能を書いた', hidden=True)
    async def all_role(self, ctx):
        try:
            all_role = [member for member in ctx.message.guild.roles[::-1]]
            list_roles = "".join([f"{k+1}:{member.mention}\n" for member, k in zip(all_role, range(0, len(all_role)))])
            ranking_msgs = ["\n".join(list_roles.split("\n")[i:i + 50]) for i in range(0, len(all_role), 50)]
            index = 0
            while True:
                msg = await ctx.send(embed=discord.Embed(title=f"{ctx.message.guild.name}の全役職情報:", description=ranking_msgs[index]).set_footer(text=f"この鯖の役職の合計の数は[{len(ctx.message.guild.roles)}]です！"))
                ll = index != 0
                r = index != len(ranking_msgs) - 1
                if ll:
                    await msg.add_reaction(left)
                if r:
                    await msg.add_reaction(right)
                react = await self.bot.wait_for('reaction_add', timeout=10, check=predicate(msg, ctx.message.author, ll, r, self.bot))
                if react[0].emoji == left:
                    index -= 1
                if react[0].emoji == right:
                    index += 1
                await msg.delete()
        except asyncio.TimeoutError:
            pass

    @commands.command(name='self-role', description='このBOTのすべての機能を書いた', hidden=True)
    async def author_role(self, ctx):
        try:
            all_role = [r.mention for r in ctx.message.author.roles][::-1]
            list_roles = "".join([f"{k+1}:{member}\n" for member, k in zip(all_role, range(0, len(all_role)))])
            ranking_msgs = ["\n".join(list_roles.split("\n")[i:i + 50]) for i in range(0, len(all_role), 50)]
            index = 0
            while True:
                msg = await ctx.send(embed=discord.Embed(title=f"{ctx.message.author}に付与されてる役職一覧:", description=ranking_msgs[index]).set_thumbnail(url="https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(ctx.message.author)))
                ll = index != 0
                r = index != len(ranking_msgs) - 1
                if ll:
                    await msg.add_reaction(left)
                if r:
                    await msg.add_reaction(right)
                react = await self.bot.wait_for('reaction_add', timeout=10, check=predicate(msg, ctx.message.author, ll, r, self.bot))
                if react[0].emoji == left:
                    index -= 1
                if react[0].emoji == right:
                    index += 1
                await msg.delete()
        except asyncio.TimeoutError:
            pass

    @commands.command(name='a', hidden=True)
    async def announce(self, ctx):
        if ctx.message.channel.id in [366373818064830465, 634757295410118656, 636330432702447657] and ctx.message.author.id in admin_id:
            await ctx.message.delete()
            message1 = await ctx.send("announceしたい内容を書いてください。")
            react = await self.bot.wait_for('message', check=lambda message: message.author == ctx.author)
            if react:
                await message1.delete()
                message2 = await ctx.send("この内容をannounceするかしないか？")
                await message2.add_reaction(no)
                await message2.add_reaction(ok)
                react1 = await self.bot.wait_for('reaction_add', timeout=10, check=predicate1(message2, ctx.message.author, self.bot))
                if react1[0].emoji == ok:
                    await message2.delete()
                    if any([True for s in ['.jpg', '.png', '.jpeg', '.tif', '.tiff', '.bmp', '.gif', '.mp4'] if s in react.content]):
                        embed = discord.Embed(timestamp=react.created_at)
                        embed.set_image(url=react.content)
                    elif react.attachments and react.content:
                        embed = discord.Embed(description=f"発言鯖:{react.guild.name} | チャンネル:{react.channel.name}\n\n{react.content}", timestamp=react.created_at)
                        embed.set_image(url=react.attachments[0].url)
                    elif react.attachments:
                        embed = discord.Embed(timestamp=react.created_at)
                        embed.set_image(url=react.attachments[0].url)
                    else:
                        embed = discord.Embed(description=f"発言鯖:{react.guild.name} | チャンネル:{react.channel.name}\n\n{react.content}", timestamp=react.created_at)
                    embed.set_author(name="TAOアナウンス!!!", icon_url=react.guild.icon_url)
                    embed.set_footer(text=react.author, icon_url=react.author.avatar_url)
                    for channel_id in [634755270626639882, 338151444731658240]:
                        await self.bot.get_channel(channel_id).send(embed=embed)
                    return await asyncio.gather(*(c.send(embed=embed) for c in self.bot.get_all_channels() if c.name == 'tao-global'))

                if react1[0].emoji == no:
                    await message2.delete()

    @commands.command(name='roles', description='取得', pass_context=True)
    async def roles(self, ctx):
        reactions = ["0⃣", "1⃣", "2⃣", "3⃣"]
        rank_list = ["月島", "幸せの猫遭遇", "チャイナ", "雪の精霊"]
        text = ""
        if ctx.message.guild.id == 337524390155780107:
            reactions.append("4⃣")
            rank_list.append("ドロキンうんち")
        for rankings in zip(reactions, rank_list):
            text += f"{rankings[0]}：`{rankings[1]}`\n"

        embed = discord.Embed(description=text)
        embed.set_author(name="報告役職一覧:")
        msg = await ctx.send(embed=embed)
        for react in reactions:
            await msg.add_reaction(react)

        def check(_, user):
            return user == ctx.message.author
        try:
            guess = await self.bot.wait_for('reaction_add', timeout=10, check=check)
            if f"{guess[0].emoji}" in reactions:
                num = re.sub("\\D", "", f"{guess[0].emoji}")
                role = discord.utils.get(ctx.message.guild.roles, name=f"{rank_list[int(num)]}報告OK")
                if role not in ctx.message.guild.roles:
                    await ctx.message.guild.create_role(name=f"{rank_list[int(num)]}報告OK", mentionable=True)
                    return await ctx.send(f"この鯖には{rank_list[int(num)]}報告OKの役職がなかったので勝手に作成したよ！\nもう一度コマンド打ってね！")
                await ctx.message.author.add_roles(role)
                return await ctx.send(f"{role.name}役職を{ctx.message.author.mention}さんに付与しました。")
        except asyncio.TimeoutError:
            pass

    @commands.command(name='minecraft', pass_context=True)
    async def minecraft(self, ctx):
        role = discord.utils.get(ctx.message.guild.roles, name=f"minecraft")
        if role not in ctx.message.guild.roles:
            await ctx.message.guild.create_role(name=f"minecraft", mentionable=True)
        await ctx.message.author.add_roles(role)
        return await ctx.send(f"minecraft役職を{ctx.message.author.mention}さんに付与しました。")

    @commands.command(name='list', description='鯖一覧取得', pass_context=True)
    @commands.has_permissions(administrator=True)
    async def lists(self, ctx):
        async with aiomysql.connect(host="localhost", user="root", db="role", password="") as conn:
            async with conn.cursor() as cur:
                server_id = ctx.message.guild.id
                if not await cur.execute('SELECT 1 FROM roles WHERE server_id=%s;', (server_id,)):
                    embed = discord.Embed(description="この鯖にはレベル役職が登録されてません。")
                    return await ctx.send(embed=embed)

                await cur.execute('SELECT lower,upper,role_id FROM roles WHERE server_id=%s ORDER BY lower;', (server_id,))
                all_list = await cur.fetchall()
                list_roles = "".join([f"`[{k+1}]: Lv{member[0]}~{member[1]}:『{discord.utils.get(ctx.message.guild.roles,id=member[2]).name}』`\n" for member, k in zip(all_list, range(0, len(all_list)))])
                ranking_msgs = ["\n".join(list_roles.split("\n")[i:i + 25]) for i in range(0, len(all_list), 25)]
                for row in ranking_msgs:
                    await ctx.send(embed=discord.Embed(description=row).set_author(name="現在の役職リストはこちら"))

    @commands.command(name='reset', description='鯖一覧取得', pass_context=True)
    @commands.has_permissions(administrator=True)
    async def reset(self, ctx):
        embeds = discord.Embed(description=f"{ctx.message.author.mention}さん\nレベル役職の設定をすべてリセットしてもいいですか？")
        msg = await ctx.send(embed=embeds)
        await msg.add_reaction(no)
        await msg.add_reaction(ok)
        try:
            react = await self.bot.wait_for('reaction_add', timeout=20, check=predicate1(msg, ctx.message.author, self.bot))
            if react[0].emoji == ok:
                async with aiomysql.connect(host="localhost", user="root", db="role", password="") as conn:
                    async with conn.cursor() as cur:
                        await cur.execute('delete from roles WHERE server_id=%s', (ctx.message.guild.id,))
                        await conn.commit()

                embed = discord.Embed(description=f"{ctx.message.author.mention}はレベル役職の設定を全てリセットしました。")
                return await ctx.send(embed=embed)

            elif react[0].emoji == no:
                embeds = discord.Embed(description=f"{ctx.message.author.mention}はレベル役職の設定をリセットしませんでした！")
                return await ctx.send(embed=embeds)

        except asyncio.TimeoutError:
            embeds = discord.Embed(description=f"{ctx.message.author.mention}はレベル役職の設定をリセットしませんでした！")
            return await ctx.send(embed=embeds)

    @commands.command(name='level', description='鯖一覧取得', pass_context=True)
    @commands.has_permissions(administrator=True)
    async def role_level(self, ctx, *args):
        server_id = ctx.message.guild.id
        if not args[0] and not args[1]:
            embed = discord.Embed(description=f"{ctx.message.author.mention}さん！\n数値を入力してください！\n例:[&level 1 10 aaa]")
            return await ctx.send(embed=embed)
        if not args[2]:
            embed = discord.Embed(description=f"{ctx.message.author.mention}さん！\n役職の名前を入力してください！\n例:[&level 1 10 aaa]")
            return await ctx.send(embed=embed)

        role_name = ""
        if len(args) >= 3:
            count = 0
            for content in args:
                if count >= 2:
                    role_name += f"{content} "
                count += 1
            role_name = role_name[:-1]
        else:
            role_name += f"{args[2]}"
        role = discord.utils.get(ctx.message.guild.roles, name=role_name)
        if not role:
            embed = discord.Embed(description=f"{ctx.message.author.mention}さん！\nどうやらこの名前の役職はこの鯖には存在しないようです！")
            return await ctx.send(embed=embed)

        embeds = discord.Embed(description=f"```『{role.name}』役職が[{args[0]}~{args[1]}Lv]の間に設定しようとしています！\n大丈夫ですか？```")
        msg = await ctx.send(embed=embeds)
        await msg.add_reaction(no)
        await msg.add_reaction(ok)
        try:
            react = await self.bot.wait_for('reaction_add', timeout=20, check=predicate1(msg, ctx.message.author, self.bot))
            if react[0].emoji == ok:
                async with aiomysql.connect(host="localhost", user="root", db="role", password="") as conn:
                    async with conn.cursor() as cur:
                        if await cur.execute('SELECT 1 FROM roles WHERE server_id=%s AND lower<=%s AND upper>=%s;', (server_id, int(args[0]), int(args[0]))) or await cur.execute('SELECT 1 FROM roles WHERE server_id=%s AND lower<=%s AND upper>=%s;', (server_id, int(args[1]), int(args[1]))):
                            embed = discord.Embed(description=f"{ctx.message.author.mention}さん\nこの役職のレベルの範囲は既に設定されています...")
                            return await ctx.send(embed=embed)
                        elif await cur.execute('SELECT 1 FROM roles WHERE server_id=%s AND role_id=%s;', (server_id, role.id)):
                            embed = discord.Embed(description=f"{ctx.message.author.mention}さん\nこの役職は既に設定されています...")
                            return await ctx.send(embed=embed)
                        else:
                            await cur.execute("INSERT INTO roles VALUES(%s,%s,%s,%s);", (server_id, int(args[0]), int(args[1]), role.id))
                            await conn.commit()
                            embed = discord.Embed(description=f"`『{role.name}』役職が[{args[0]}~{args[1]}Lv]の間に設定されました。`")
                            return await ctx.send(embed=embed)

            elif react[0].emoji == no:
                embeds = discord.Embed(description=f"{ctx.message.author.mention}はレベル役職を設定しませんでした！")
                return await ctx.send(embed=embeds)

        except asyncio.TimeoutError:
            embeds = discord.Embed(description=f"{ctx.message.author.mention}はレベル役職を設定しませんでした！")
            return await ctx.send(embed=embeds)

    @commands.Cog.listener()
    async def on_message(self, message, level=None, role_name=None):
        try:
            if isinstance(message.channel, discord.DMChannel) and message.author != self.bot.user:
                return await message.channel.send(embed=discord.Embed(description=f"{message.author.mention}さん。\nこのBOTはDM対応外です...", color=0xC41415))

            if message.channel.id == 668071221165817894:
                return await message.publish()

            if len(message.embeds) != 0 and message.author.id == 526620171658330112 and message.embeds[0].title:
                if "のステータス" in message.embeds[0].title[-7:]:
                    for f in message.embeds[0].fields:
                        if f.name == "Lv":
                            level = int(f.value)

                    member = discord.utils.get(message.guild.members, display_name=message.embeds[0].title[:-7])
                    role_level = {}
                    async with aiomysql.connect(host="localhost", user="root", db="role", password="") as conn:
                        async with conn.cursor() as cur:
                            await cur.execute('SELECT lower, upper, role_id FROM roles WHERE server_id=%s ORDER BY lower;', (message.guild.id,))
                            role_list = await cur.fetchall()
                            if not role_list:
                                embeds = discord.Embed(description=f"{message.author.mention}！\nこの鯖にはレベル役職は設定されてないよ！")
                                return await message.channel.send(embed=embeds)
                            for lower, upper, role_id in role_list:
                                role = discord.utils.get(message.guild.roles, id=role_id)
                                if role is None:
                                    continue
                                max_role = role.name
                                role_level[role_id] = (lower, upper)

                    role_id = next((role_id for role_id, lu in role_level.items() if (lambda xx: lu[0] <= xx <= lu[1])(level)), None)
                    role = discord.utils.get(message.guild.roles, id=role_id)
                    next_level = 0
                    for _, upper in sorted(role_level.values()):
                        if upper > level:
                            next_level = upper + 1
                            break
                    if member:
                        if max([upper for _, upper in role_level.values()]) < level:
                            return await message.channel.send("```凄い！あなたはこの鯖の役職付与範囲を超えてしまった！\nぜひ運営に役職を追加して貰ってください！\nこの鯖の最高レベル役職は『{}』です。```".format(max_role))
                        elif member.roles and role in member.roles:
                            return await message.channel.send("`次のレベル役職まで後{}Lvです！`".format(int(next_level - level)))
                        else:
                            await member.add_roles(role)
                            await message.channel.send("`役職名:『{0}』を付与しました。\n次のレベル役職まで後{1}Lvです！`".format(role, int(next_level - level)))
                            embed = discord.Embed(title=f"{member.name}さんが役職を更新しました！", description=f"```役職名:『{role}』```")
                            embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(member))
                            embed.set_author(name=message.guild.me.name)
                            for channel in message.guild.channels:
                                if channel.name == '役職更新ログ':
                                    return await channel.send(embed=embed)

            if message.guild.id == 337524390155780107 and message.author.id == 247671415715790849:
                role = discord.utils.get(message.guild.roles, name=f"ドロキンうんち報告OK")
                return await message.channel.send(f"{role.mention}～ドロキンさんが出たらしいぜ！")

            if len(message.embeds) != 0 and message.embeds[0].title and "【超激レア】" in message.embeds[0].title and message.author.id == 526620171658330112:
                lists = re.findall(r'([0-9]+)', f"{message.embeds[0].title}")
                if "月島" in message.embeds[0].title:
                    role_name = "月島"
                elif "狂気ネコしろまる" in message.embeds[0].title:
                    role_name = "幸せの猫遭遇"
                elif "雪の精霊　ジャックフロスト" in message.embeds[0].title:
                    role_name = "雪の精霊"
                elif "チャイナ:ドット" in message.embeds[0].title:
                    role_name = "チャイナ"

                url = f"https://discordapp.com/channels/{message.guild.id}/{message.channel.id}/{message.id}"
                embed = discord.Embed(description=f"""{message.channel.mention}で{role_name}が出現しました！\n`[Lv.{int(lists[0])}]`の{role_name}が出現しました！\n敵の体力は`[HP:{int(lists[1])}]`\n\nゲットできる経験値数は`[{(int(lists[0]) * 100)}]`です！\n\n[**この{role_name}への直通リンク**](<{url}>)""", timestamp=message.created_at)
                embed.set_thumbnail(url=message.embeds[0].image.url)
                role = discord.utils.get(message.guild.roles, name=f"{role_name}報告OK")
                if role not in message.guild.roles:
                    await message.guild.create_role(name=f"{role_name}報告OK", mentionable=True)
                    await message.channel.send(f"この鯖には{role_name}報告OKの役職がなかったから勝手に作成したよ！")
                for channel in message.guild.channels:
                    if channel.name == f'超激レア出現ログ':
                        await channel.send(embed=embed)
                        return await channel.send(f"{role.mention}～{role_name}出たらしいぜ！")

            if any([True for s in ["DISCORD.GG", "DISBOARD.ORG", "BIT.LY", "DISCORDAPP", "INVITE.GG", "DISCORD.COM"] if s in message.content.upper()]):
                if message.author.id in [304932786286886912, 460208854362357770, 574166391071047694, 294362309558534144] or message.author.bot:
                    return
                if message.guild.id == 337524390155780107 and not (message.channel.id in [421954703509946368, 539805974672834570, 645178648474943489]):
                    channel = self.bot.get_channel(421954703509946368)
                    await message.delete()
                    embed = discord.Embed(title="このチャンネルでは宣伝は禁止です！", description="{0}さん\nもし鯖の宣伝をしたいなら{1}でやってください！".format(message.author.mention, channel.mention))
                    return await message.channel.send(embed=embed)

            if message.channel.name == "tao-global":
                async with aiomysql.connect(host="localhost", user="root", db="role", password="") as conn:
                    async with conn.cursor() as cur:
                        if await cur.execute('SELECT 1 FROM get WHERE author_id=%s;', (message.author.id,)) or message.author == self.bot.user or message.author.bot and message.author.id != 526620171658330112:
                            return
                        elif message.embeds and message.embeds[0]:
                            return await message.channel.send(embed=message.embeds[0])
                        elif any([True for s in ['.jpg', '.png', '.jpeg', '.tif', '.tiff', '.bmp', '.gif', '.mp4'] if s in message.content]):
                            embed = discord.Embed(timestamp=message.created_at)
                            embed.set_image(url=message.content)
                        elif message.attachments and message.content:
                            embed = discord.Embed(description=message.content, timestamp=message.created_at)
                            embed.set_image(url=message.attachments[0].url)
                        elif message.attachments:
                            embed = discord.Embed(timestamp=message.created_at)
                            embed.set_image(url=message.attachments[0].url)
                        else:
                            embed = discord.Embed(description=message.content, timestamp=message.created_at)
                        embed.set_author(name=message.guild.name, icon_url="https://cdn.discordapp.com/icons/{0.id}/{0.icon}.png?size=1024".format(message.guild))
                        embed.set_footer(text=message.author, icon_url="https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(message.author))
                        await message.delete()
                        try:
                            return await asyncio.gather(*(c.send(embed=embed) for c in self.bot.get_all_channels() if c.name == 'tao-global'))
                        except Exception as _:
                            pass

        except discord.errors.Forbidden:
            return

        except Exception as error:
            text = ""
            for x in traceback.format_exception(type(error), error, error.__traceback__):
                x = x.replace(f"\\{getpass.getuser()}\\", "\\*\\")
                if len(text + x) < 2000 - 20:
                    text += x
                else:
                    await self.bot.get_channel(635114963698188298).send(embed=discord.Embed(description=f"```py\n{text}```", timestamp=message.created_at))
                    text = x
            await self.bot.get_channel(635114963698188298).send(embed=discord.Embed(description=f"```py\n{text}```", timestamp=message.created_at))

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        try:
            if before.guild.id == 337524390155780107:
                if any([True for s in ["DISCORD.GG", "DISBOARD.ORG", "BIT.LY", "DISCORDAPP", "INVITE.GG", "DISCORD.COM"] if s in after.content.upper()]) and not before.author.bot and before.channel.id != 421954703509946368:
                    channel = self.bot.get_channel(657769986303066113)
                    embed = discord.Embed(title="このチャンネルでは宣伝は禁止です！", description="{0}さん\nもし鯖の宣伝をしたいなら{1}でやってください！".format(after.author.mention, channel.mention))
                    await after.author.send(embed=embed)
                    return await after.delete()
        except AttributeError:
            pass


def setup(bot):
    bot.add_cog(Bots(bot))

import discord
from discord.ext import commands
import os
import asyncio
import re
from dotenv import load_dotenv

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Configuration des intents (Permissions requises par l'API Discord)
intents = discord.Intents.default()
intents.message_content = True  # Requis pour lire le contenu des messages et détecter le préfixe
intents.members = True          # Requis pour bannir/expulser et gérer les membres

# Initialisation du bot avec le préfixe '+'
bot = commands.Bot(command_prefix="+", intents=intents, help_command=None)

# --- Fonctions Utilitaires ---

def parse_duration(duration_str: str) -> int:
    """ Convertit une chaîne de durée (ex: 10s, 5m, 2h, 1d) en secondes. """
    match = re.match(r"^(\d+)([smhd])$", duration_str.lower())
    if not match:
        return -1
    
    amount = int(match.group(1))
    unit = match.group(2)
    
    if unit == 's':
        return amount
    elif unit == 'm':
        return amount * 60
    elif unit == 'h':
        return amount * 3600
    elif unit == 'd':
        return amount * 86400
    return -1

# --- Événements ---

@bot.event
async def on_ready():
    print(f"=========================================")
    print(f" Bot connecté avec succès !")
    print(f" Nom d'utilisateur : {bot.user.name}")
    print(f" ID du Bot : {bot.user.id}")
    print(f" Préfixe configuré : +")
    print(f"=========================================")
    # Définir l'activité du bot
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="le serveur | +help"))

# --- Commandes ---

@bot.command(name="help")
async def help_command(ctx):
    """Affiche la liste des commandes disponibles."""
    embed = discord.Embed(
        title="📚 Liste des Commandes du Bot",
        description="Voici les commandes disponibles. Le préfixe est `+`.",
        color=discord.Color.blue()
    )
    
    embed.add_field(
        name="🛠️ Modération",
        value=(
            "`+clear <nombre>` : Supprime un nombre spécifique de messages dans le salon.\n"
            "`+kick <@membre> [raison]` : Expulse un membre du serveur.\n"
            "`+ban <@membre> [raison]` : Bannit un membre définitivement.\n"
            "`+tempban <@membre> <durée> [raison]` : Bannit temporairement un membre (ex: `10m`, `2h`, `1d`)."
        ),
        inline=False
    )
    
    embed.add_field(
        name="🎨 Utilitaire",
        value=(
            "`+embed <titre> | [description] | [couleur_hex] | [image_url]` : Crée un embed personnalisé.\n"
            "*(Séparez les arguments par une barre verticale `|`)*"
        ),
        inline=False
    )
    
    embed.set_footer(text=f"Demandé par {ctx.author.name}", icon_url=ctx.author.avatar.url if ctx.author.avatar else None)
    await ctx.send(embed=embed)


@bot.command(name="embed")
@commands.has_permissions(manage_messages=True)
async def embed_command(ctx, *, args: str):
    """
    Crée un embed personnalisé.
    Syntaxe : +embed Titre | Description | #Couleur | URL de l'image
    """
    # Diviser les arguments par la barre verticale "|"
    parts = [p.strip() for p in args.split("|")]
    
    title = parts[0]
    description = parts[1] if len(parts) > 1 else ""
    color_hex = parts[2] if len(parts) > 2 else "#3498db"
    image_url = parts[3] if len(parts) > 3 else None

    # Conversion de la couleur hexadécimale en objet discord.Color
    try:
        if color_hex.startswith("#"):
            color_hex = color_hex[1:]
        color = discord.Color(int(color_hex, 16))
    except ValueError:
        color = discord.Color.blue()  # Couleur par défaut en cas d'erreur

    # Création de l'embed
    embed = discord.Embed(title=title, description=description, color=color)
    
    if image_url:
        embed.set_image(url=image_url)
        
    embed.set_footer(text=f"Posté par {ctx.author.name}", icon_url=ctx.author.avatar.url if ctx.author.avatar else None)
    
    # Supprimer le message d'origine de l'utilisateur
    try:
        await ctx.message.delete()
    except discord.Forbidden:
        pass

    await ctx.send(embed=embed)


@bot.command(name="clear")
@commands.has_permissions(manage_messages=True)
async def clear_command(ctx, amount: int):
    """Supprime un nombre donné de messages dans le salon."""
    if amount <= 0:
        await ctx.send("❌ Veuillez spécifier un nombre supérieur à 0.", delete_after=5)
        return
        
    # On ajoute 1 pour supprimer aussi le message de commande +clear
    deleted = await ctx.channel.purge(limit=amount + 1)
    await ctx.send(f"✅ **{len(deleted) - 1}** messages ont été supprimés.", delete_after=5)


@bot.command(name="kick")
@commands.has_permissions(kick_members=True)
async def kick_command(ctx, member: discord.Member, *, reason: str = "Aucune raison fournie"):
    """Expulse un membre du serveur."""
    if member.top_role >= ctx.author.top_role and ctx.guild.owner != ctx.author:
        await ctx.send("❌ Vous ne pouvez pas expulser un membre ayant un rôle supérieur ou égal au vôtre.")
        return

    await member.kick(reason=reason)
    
    embed = discord.Embed(
        title="👢 Membre Expulsé",
        description=f"**{member.mention}** a été expulsé du serveur.",
        color=discord.Color.orange()
    )
    embed.add_field(name="Modérateur", value=ctx.author.mention, inline=True)
    embed.add_field(name="Raison", value=reason, inline=True)
    await ctx.send(embed=embed)


@bot.command(name="ban")
@commands.has_permissions(ban_members=True)
async def ban_command(ctx, member: discord.Member, *, reason: str = "Aucune raison fournie"):
    """Bannit un membre définitivement du serveur."""
    if member.top_role >= ctx.author.top_role and ctx.guild.owner != ctx.author:
        await ctx.send("❌ Vous ne pouvez pas bannir un membre ayant un rôle supérieur ou égal au vôtre.")
        return

    await member.ban(reason=reason)
    
    embed = discord.Embed(
        title="🚫 Membre Banni",
        description=f"**{member.mention}** a été banni du serveur.",
        color=discord.Color.red()
    )
    embed.add_field(name="Modérateur", value=ctx.author.mention, inline=True)
    embed.add_field(name="Raison", value=reason, inline=True)
    await ctx.send(embed=embed)


@bot.command(name="tempban")
@commands.has_permissions(ban_members=True)
async def tempban_command(ctx, member: discord.Member, duration: str, *, reason: str = "Aucune raison fournie"):
    """
    Bannit temporairement un membre.
    Exemple: +tempban @pseudo 30m Spam intensif
    Durées acceptées : s (secondes), m (minutes), h (heures), d (jours).
    """
    if member.top_role >= ctx.author.top_role and ctx.guild.owner != ctx.author:
        await ctx.send("❌ Vous ne pouvez pas bannir un membre ayant un rôle supérieur ou égal au vôtre.")
        return

    seconds = parse_duration(duration)
    if seconds <= 0:
        await ctx.send("❌ Durée invalide. Utilisez un format correct : `30s`, `15m`, `2h`, `1d` (secondes, minutes, heures, jours).")
        return

    # Bannir le membre
    await member.ban(reason=f"[Tempban {duration}] {reason}")
    
    embed = discord.Embed(
        title="⏳ Membre Banni Temporairement",
        description=f"**{member.mention}** a été banni pour une durée de **{duration}**.",
        color=discord.Color.red()
    )
    embed.add_field(name="Modérateur", value=ctx.author.mention, inline=True)
    embed.add_field(name="Raison", value=reason, inline=True)
    await ctx.send(embed=embed)

    # Attendre la fin du temps imparti
    await asyncio.sleep(seconds)

    # Débannir le membre si toujours banni
    try:
        # Récupérer la liste des bans pour vérifier que l'utilisateur y figure toujours
        bans = [entry async for entry in ctx.guild.bans()]
        is_banned = any(entry.user.id == member.id for entry in bans)
        
        if is_banned:
            await ctx.guild.unban(member, reason="Fin du bannissement temporaire.")
            # Optionnel : Envoyer un message dans le salon pour signaler le débannissement
            unban_embed = discord.Embed(
                title="🔓 Débannissement Automatique",
                description=f"Le bannissement temporaire de **{member.name}#{member.discriminator}** ({member.id}) est arrivé à terme. L'utilisateur a été débanni.",
                color=discord.Color.green()
            )
            await ctx.send(embed=unban_embed)
    except discord.Forbidden:
        print(f"Erreur : Permissions insuffisantes pour débannir {member.name}.")
    except Exception as e:
        print(f"Erreur lors du débannissement : {e}")

# --- Gestion des Erreurs ---

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ Vous n'avez pas les permissions nécessaires pour utiliser cette commande.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"❌ Argument manquant. Tapez `+help` pour voir l'utilisation correcte des commandes.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("❌ Argument invalide (ex: membre introuvable ou nombre incorrect).")
    elif isinstance(error, commands.CommandNotFound):
        pass  # Ignorer si la commande n'existe pas
    else:
        # Autres erreurs de commande
        await ctx.send(f"⚠️ Une erreur est survenue lors de l'exécution de la commande.")
        print(f"Erreur : {error}")

# Lancement du bot
if __name__ == "__main__":
    if not TOKEN or TOKEN == "VOTRE_TOKEN_ICI":
        print("=========================================")
        print(" ERREUR : Le token du bot n'est pas configuré !")
        print(" Veuillez ouvrir le fichier .env et insérer votre token.")
        print("=========================================")
    else:
        try:
            bot.run(TOKEN)
        except discord.LoginFailure:
            print("=========================================")
            print(" ERREUR : Connexion échouée. Le token est invalide.")
            print(" Vérifiez le token dans votre fichier .env.")
            print("=========================================")
        except Exception as e:
            print(f"Une erreur est survenue au démarrage : {e}")

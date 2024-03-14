import discord
from discord.ext import commands
import settings

def run():
    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix="!", intents=intents)

    tasks = {}

    # Check if a task is assigned to a member
    def is_task_assigned(member):
        return member in tasks and tasks[member]

    # Define roles that can use the commands
    allowed_roles = ["president", "vice president", "hr", "tl", "manager"]
    @bot.event
    async def on_command_error(ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send("Don't try it again!")

    # Custom check to restrict commands to specified roles
    def has_allowed_role():
        async def predicate(ctx):
            author_roles = [role.name.lower() for role in ctx.author.roles]
            return any(role in allowed_roles for role in author_roles)
        return commands.check(predicate)

    @bot.command()
    @has_allowed_role()
    async def assign(ctx, member: discord.Member, *args):
        task_name = ' '.join(args[:-1])
        deadline_date = args[-1]
        tasks[member] = {'task_name': task_name, 'deadline_date': deadline_date}

        embed = discord.Embed(title="Task Assigned", description=f"**Task '{task_name}' assigned to {member.display_name} with deadline {deadline_date}**", color=discord.Color.green())
        await ctx.send(embed=embed)

    @bot.command()
    @has_allowed_role()
    async def done(ctx, member: discord.Member, *, task_name: str):
        if member in tasks and tasks[member]['task_name'] == task_name:
            tasks[member] = None
            embed = discord.Embed(title="Task Completed", description=f"**Task '{task_name}' marked as done for {member.display_name}**", color=discord.Color.blue())
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"No task '**{task_name}**' assigned to {member.display_name}. Make sure to provide the correct task name.")

    @bot.command()
    @has_allowed_role()
    async def list(ctx):
        if not tasks:
            await ctx.send("No tasks assigned to any members.")
        else:
            embed = discord.Embed(title="Task List", color=discord.Color.gold())
            for member, task_info in tasks.items():
                if task_info:
                    task_name = task_info['task_name']
                    deadline_date = task_info['deadline_date']
                    roles_str = ', '.join([role.name for role in member.roles])  # Get all roles of the member
                    embed.add_field(name=f"**{member.display_name} ({roles_str})**", value=f"**Task: {task_name}**\n**Deadline: {deadline_date}**", inline=False)
            await ctx.send(embed=embed)


    



    @bot.event
    async def on_ready():
        print(f'Logged in as {bot.user}')

    bot.run('MTIxNzYyMzIwNjExMDY5MTQwOQ.GjZUgO.YU82SvpNoNqlvnMjZovX_-TyHBAztjQqUG_AjM', root_logger=True)

if __name__ == "__main__":
    run()

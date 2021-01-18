__authors__ = 'aejb'
import json
import math
import numpy
import typing

import discord
import aiohttp
import asyncio
from discord.ext import commands, tasks
from datetime import datetime, timedelta
from random import randint
import pickledb


class apple(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    def any_apples(self, id):
        db = pickledb.load('appledb', False)
        existing_apples = db.get(str(id))
        db.dump()
        if existing_apples>=1:
            return True
        else:
            return False


    @commands.command()
    async def sniff(self, ctx):
        """------ sniffs for any apples that might be lying around"""
        sniff_roll = randint(0,4)
        if 0<=sniff_roll<=2 or self.any_apples('ground')==False:
            await ctx.send("you didn't find any apples :(")
        else:
            ground_apples = self.get_apples('ground')
            await ctx.send("you found {apples_found} apples!".format(apples_found=ground_apples))
            self.give_apples(ctx.author.id, ground_apples)
            self.give_apples('ground', int(-1*ground_apples))

    @commands.command()
    async def throw(self, ctx, thrown_at: discord.Member):
        """------ throw an apple at a friend (with a mention!)"""
        throw_roll = randint(0,3)
        if self.any_apples(ctx.author.id)==False:
            await ctx.send("you haven't got any apples to throw :(")
            return
        self.give_apples(ctx.author.id, -1)
        if throw_roll == 0:
            await ctx.send("you missed, sorry :(")
            self.give_apples('ground', 1)
        elif throw_roll == 1:
            await ctx.send("{thrown_at_mention} caught the apple!".format(thrown_at_mention=thrown_at.mention))
            self.give_apples(thrown_at.id, 1)
        else:
            await ctx.send("you hit {thrown_at_mention} with an apple.... which disappeared".format(thrown_at_mention=thrown_at.mention))

    @commands.command()
    async def count(self, ctx):
        """------ tells you how many apples you have"""
        db = pickledb.load('appledb', False)
        apple_count = db.get(str(ctx.author.id))
        if apple_count == False:
            await ctx.send("you don't have any apples :(")
        else:
            await ctx.send("you've got {count} apples!".format(count=str(apple_count)))
        db.dump()

    @commands.command()
    async def pls(self, ctx):
        """------ looks for apples"""
        roll = randint(1, 101)
        if roll == 1 or roll == 2:
            await ctx.send("woah! you found an extra shiny apple! that's worth four apples!✨🍎✨")
            self.give_apples(ctx.author.id, 4)
        elif roll == 3:
            await ctx.send("oh my god you found a GOLD APPLE! that's worth SEVEN apples! 🌟🌟🍎🌟🌟")
            self.give_apples(ctx.author.id, 7)
        elif 4 <= roll <= 14:
            await ctx.send("hey nice apple! that's gotta be worth three apples! 💫🍎💫")
            self.give_apples(ctx.author.id, 3)
        elif roll == 15 or roll == 16:
            await ctx.send("oh dear. you found a rotten apple :( you let another apple go bad! 🤢🍎🤢")
            self.give_apples(ctx.author.id, -1)
        elif 17 <= roll <= 25:
            await ctx.send("oh neat! two apples! 🍎🍎")
            self.give_apples(ctx.author.id, 2)
        elif 26 <= roll <= 30:
            await ctx.send("you found a green apple. it is the enemy. remove it at once. 🚫🍏🚫")
        elif 31<=roll<=80:
            await ctx.send("here u go: 🍎")
            self.give_apples(ctx.author.id, 1)
        else:
            await ctx.send("no apples, sorry :(")

    def give_apples(self, id, new_apples):
        db = pickledb.load('appledb', False)
        existing_apples = db.get(str(id))
        total_apples = existing_apples+new_apples
        db.set(str(id), total_apples)
        db.dump()

    def get_apples(self, id):
        db = pickledb.load('appledb', False)
        existing_apples = db.get(str(id))
        db.dump()
        return existing_apples


def setup(bot):
    bot.add_cog(apple(bot))

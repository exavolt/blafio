#!/usr/bin/env python

from tornado.options import define as opt


opt("config", default=None, help=
    "Config file name to load")
opt("daemon", default=False, type=bool, help=
    "Run as daemon")

opt("host", default="", help=
    "Listen to the specified host")
opt("port", default=11002, type=int, help=
    "Run on the given port")

opt("db_name", default="blafio", help=
    "DB Name")
opt("db_host", default=None, help=
    "DB server address")
opt("db_port", default=None, type=int, help=
    "DB server port")
opt("db_usr", default=None, help=
    "DB username")
opt("db_pwd", default=None, help=
    "DB password")


if __name__ == "__main__":
    #TODO: Generate template with docs
    pass


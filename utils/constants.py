IGNORED_ERRORS = [
    "admin", "gifadd", "gifdelete", "restart", "logs", "log_latest", "kill",
    "poke",
    "comicsblog",
    "getcomics",
    "gif",
    "google", "googlelist",
    "header",
    "help",
    "kick", "ban", "nomorespoil",
    "recrutement", "timer", "choose","coinflip", "say", "edit", "roulette",
    "team", "clear",
    "urban",
    "youtube", "youtubelist"
    ]

IGNORE_COMMAND_NOT_FOUND = [f'Command "{command}" is not found'
                            for command in IGNORED_ERRORS]

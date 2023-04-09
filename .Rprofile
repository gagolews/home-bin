# Copyleft (C) 2002-2023, Marek Gagolewski <https://www.gagolewski.com>

# This file is sourced by ~/.Rprofile.

if (interactive()) {
    # defaults:
    # prompt="> "
    # continue="+ "
    # digits=7
    # max.print=99999
    # scipen=0
    # timeout=60
    # useFancyQuotes
    # width=80

    options(digits=5)
    options(scipen=5)
    options(timeout=120)
    # options(stringsAsFactors=FALSE)  # default in R 4.0
    options(max.print=999)
    options(useFancyQuotes=FALSE)
    options(width=110)
    # options(warnPartialMatchArgs=TRUE)
    # options(warnPartialMatchAttr=TRUE)
    # options(warnPartialMatchDollar=TRUE)
    options(help_type="html")

    .marekstuff <- new.env()

    .marekstuff$unload <- function(pkg, verbose=TRUE) {
        ppkg <- paste0("package:", pkg)
        if (ppkg %in% search()) {
            dynlib <- grep(sapply(.dynLibs(), "[[", "name"), pattern=pkg)
            if (length(dynlib) == 1L)
                library.dynam.unload(
                    pkg,
                    libpath=sub("/Meta.*", '', attr(packageDescription(pkg), "file"))
                )
            detach(ppkg, character.only=TRUE, unload=TRUE, force=TRUE)
            if (isTRUE(verbose)) message(sprintf("%s has been unloaded", ppkg))
        }
        else {
            if (isTRUE(verbose)) message(sprintf("%s has not been loaded; nothing to do", ppkg))
        }
    }

    .marekstuff$reload <- function(pkg, verbose=TRUE) {
        ppkg <- paste0("package:", pkg)
        if (ppkg %in% search()) {
            unload(pkg, verbose=FALSE)
            library(pkg, character.only=TRUE)
            if (isTRUE(verbose)) message(sprintf("%s has been reloaded", ppkg))
        }
        else {
            library(pkg, character.only=TRUE)
            if (isTRUE(verbose)) message(sprintf("%s has been loaded", ppkg))
        }
    }

    attr(.marekstuff, "name") <- ".marekstuff"
    suppressMessages(attach(.marekstuff, pos=2L, name=".marekstuff"))
    rm(".marekstuff")

    .First <- function() {
        cat(sprintf(
            "# R %s.%s [using ~/.Rprofile] [marekstuff: %s]\n",
            R.Version()$major,
            R.Version()$minor,
            paste0(ls(envir=as.environment(".marekstuff")), collapse=", ")
        ))
    }

}

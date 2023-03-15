# Copyleft (C) 2020-2023, Marek Gagolewski <https://www.gagolewski.com>

library("knitr")
options(encoding="UTF-8")
opts_chunk$set(
    fig.width=5.9375,    # /1.25 = (textwidth=4.75)
    out.width=5.9375,
    fig.height=3.4635,  # fig.width/(12/7)
    dpi=240,            # *1.5 = 300
    dev=c("CairoSVG", "CairoPDF"),
    error=FALSE,
    fig.show="hold",
    results="hold",
    fig.lp='fig:',
    dev.args=list(pointsize=11),
    comment="##",
    cache.comments=TRUE
)

knit_hooks$set(plot=knitr:::hook_plot_md_pandoc)
set.seed(666)

options(encoding="UTF-8")
options(width=74)
options(digits=5)
options(stringsAsFactors=FALSE)  # default in R 4.0
options(max.print=99)
options(useFancyQuotes=FALSE)

options(warnPartialMatchArgs=TRUE)
options(warnPartialMatchAttr=TRUE)
options(warnPartialMatchDollar=TRUE)


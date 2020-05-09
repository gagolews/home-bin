# Copyright (C) 2020, Marek Gagolewski, https://www.gagolewski.com

library("knitr")
options(encoding="UTF-8")
opts_chunk$set(
    fig.height=3.5,
    fig.width=6,
    dev=c("CairoSVG"),
    out.width=NULL,
    dpi=300,
    error=FALSE,
    fig.show="hold",
    fig.lp='fig:',
    dev.args=list(pointsize=11)
)

knit_hooks$set(plot=knitr:::hook_plot_md_pandoc)
set.seed(666)
options(width=64)
options(digits=7)

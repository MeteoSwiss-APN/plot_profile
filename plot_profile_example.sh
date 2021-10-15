# show help
echo Test1
plot_profile --help

# defaul plot example
echo Test2
plot_profile

# show various possible plots
echo Test3
plot_profile --date 2021083100 --alt_bot 500 --alt_top 3000 --clouds --outpath exp1/ # all-in-one plot
plot_profile --date 2021083100 --alt_bot 500 --alt_top 3000 --clouds --outpath exp1/ --params temp --params 747 # temp plot
plot_profile --date 2021083100 --alt_bot 500 --alt_top 3000 --clouds --outpath exp1/ --params 743 # winddir plot
plot_profile --date 2021083100 --alt_bot 500 --alt_top 3000 --clouds --outpath exp1/ --params 748 # windvel plot

# show the plots using pre-defined standard settings
echo Test4
plot_profile --date 2021083000 --alt_bot 1000 --alt_top 5000 --clouds --grid --outpath exp1/ --standard_settings
plot_profile --date 2021083000 --alt_bot 1000 --alt_top 5000 --clouds --outpath exp1/ --standard_settings --params dewp --params temp
plot_profile --date 2021083000 --alt_bot 1000 --alt_top 5000 --clouds --outpath exp1/ --standard_settings --params winddir
plot_profile --date 2021083000 --alt_bot 1000 --alt_top 5000 --clouds --outpath exp1/ --standard_settings --params windvel --params winddir

# show the plots using personal settings
echo Test5
plot_profile --date 2021082900 --alt_bot 1000 --alt_top 5000 --clouds --outpath exp1/ --personal_settings --temp_min '-30' --temp_max 30 --windvel_min 0 --windvel_max 30

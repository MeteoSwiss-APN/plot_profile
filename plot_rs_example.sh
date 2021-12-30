# echo 'plot_rs'
# plot_rs --help

echo 'Single Plot Cases'
plot_rs --date 2021111012 --outpath plots/single --alt_bot 1000 --alt_top 3000 --params wind_vel
plot_rs --date 2021111012 --outpath plots/single --alt_bot 1000 --alt_top 3000 --params wind_dir
plot_rs --date 2021111012 --outpath plots/single --alt_bot 1000 --alt_top 3000 --params temp
plot_rs --date 2021111012 --outpath plots/single --alt_bot 1000 --alt_top 3000 --params dewp_temp
plot_rs --date 2021111012 --outpath plots/single --alt_bot 1000 --alt_top 3000 --params temp --params dewp_temp
plot_rs --date 2021111012 --outpath plots/single --alt_bot 1000 --alt_top 3000 --params dewp_temp --params temp

echo 'Temperature and Dew Point Plots for various settings'
# dynamic x-axis
plot_rs --date 2021111012 --outpath plots/dynamic/temp --alt_bot 1000 --alt_top 3000 --params temp
plot_rs --date 2021111012 --outpath plots/dynamic/temp --alt_bot 1000 --alt_top 3000 --params dewp_temp
plot_rs --date 2021111012 --outpath plots/dynamic/temp --alt_bot 1000 --alt_top 3000 --params temp --params dewp_temp

# standard x-axis
plot_rs --date 2021111012 --outpath plots/standard/temp --alt_bot 1000 --alt_top 3000 --params temp --standard_settings
plot_rs --date 2021111012 --outpath plots/standard/temp --alt_bot 1000 --alt_top 3000 --params dewp_temp --standard_settings
plot_rs --date 2021111012 --outpath plots/standard/temp --alt_bot 1000 --alt_top 3000 --params temp --params dewp_temp --standard_settings

# personal x-axis
plot_rs --date 2021111012 --outpath plots/personal/temp --alt_bot 1000 --alt_top 3000 --params temp --personal_settings --temp_min -10 --temp_max 10
plot_rs --date 2021111012 --outpath plots/personal/temp --alt_bot 1000 --alt_top 3000 --params dewp_temp --personal_settings --temp_min -10 --temp_max 10
plot_rs --date 2021111012 --outpath plots/personal/temp --alt_bot 1000 --alt_top 3000 --params temp --params dewp_temp --personal_settings --temp_min -10 --temp_max 10


echo 'Wind Velocity and Wind Direction Plots for various settings'
# dynamic x-axis
plot_rs --date 2021111012 --outpath plots/dynamic/wind --alt_bot 1000 --alt_top 3000 --params wind_dir
plot_rs --date 2021111012 --outpath plots/dynamic/wind --alt_bot 1000 --alt_top 3000 --params wind_vel
plot_rs --date 2021111012 --outpath plots/dynamic/wind --alt_bot 1000 --alt_top 3000 --params wind_dir --params wind_vel

# standard x-axis
plot_rs --date 2021111012 --outpath plots/standard/wind --alt_bot 1000 --alt_top 3000 --params wind_dir --standard_settings
plot_rs --date 2021111012 --outpath plots/standard/wind --alt_bot 1000 --alt_top 3000 --params wind_vel --standard_settings
plot_rs --date 2021111012 --outpath plots/standard/wind --alt_bot 1000 --alt_top 3000 --params wind_dir --params wind_vel --standard_settings

# personal x-axis
plot_rs --date 2021111012 --outpath plots/personal/wind --alt_bot 1000 --alt_top 3000 --params wind_dir --personal_settings --windvel_min 5 --windvel_max 30
plot_rs --date 2021111012 --outpath plots/personal/wind --alt_bot 1000 --alt_top 3000 --params wind_vel --personal_settings --windvel_min 5 --windvel_max 30
plot_rs --date 2021111012 --outpath plots/personal/wind --alt_bot 1000 --alt_top 3000 --params wind_dir --params wind_vel --personal_settings --windvel_min 5 --windvel_max 30


echo 'Wind Direction, Temperature & Dew Point Plots for various settings'
# dynamic x-axis
plot_rs --date 2021111012 --outpath plots/dynamic/winddir_temp_dewp --alt_bot 1000 --alt_top 3000 --params wind_dir --params dewp_temp --params temp
# standard x-axis
plot_rs --date 2021111012 --outpath plots/standard/winddir_temp_dewp --alt_bot 1000 --alt_top 3000 --params wind_dir --params dewp_temp --params temp --standard_settings
# personal x-axis
plot_rs --date 2021111012 --outpath plots/personal/winddir_temp_dewp --alt_bot 1000 --alt_top 3000 --params wind_dir --params dewp_temp --params temp --personal_settings --temp_min -20 --temp_max 30

echo 'Wind Direction & Temperature Plots for various settings'
# dynamic x-axis
plot_rs --date 2021111012 --outpath plots/dynamic/winddir_temp --alt_bot 1000 --alt_top 3000 --params wind_dir --params temp
# standard x-axis
plot_rs --date 2021111012 --outpath plots/standard/winddir_temp --alt_bot 1000 --alt_top 3000 --params wind_dir --params temp --standard_settings
# personal x-axis
plot_rs --date 2021111012 --outpath plots/personal/winddir_temp --alt_bot 1000 --alt_top 3000 --params wind_dir --params temp --personal_settings --temp_min -20 --temp_max 30

echo 'Wind Direction & Dew Point Plots for various settings'
# dynamic x-axis
plot_rs --date 2021111012 --outpath plots/dynamic/winddir_dewp --alt_bot 1000 --alt_top 3000 --params wind_dir --params dewp_temp
# standard x-axis
plot_rs --date 2021111012 --outpath plots/standard/winddir_dewp --alt_bot 1000 --alt_top 3000 --params wind_dir --params dewp_temp --standard_settings
# personal x-axis
plot_rs --date 2021111012 --outpath plots/personal/winddir_dewp --alt_bot 1000 --alt_top 3000 --params wind_dir --params dewp_temp --personal_settings --temp_min -20 --temp_max 30

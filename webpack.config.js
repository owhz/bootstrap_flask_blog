const path = require("path");

const webpack = require("webpack");
const CleanWebpackPlugin = require("clean-webpack-plugin");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const ManifestRevisionPlugin = require("manifest-revision-webpack-plugin");

const devMode = (process.env.NODE_ENV !== "production");
const rootAssetPath = path.join(__dirname, "./assets/");
const buildPath = path.join(__dirname, "./app/static/build/");
const publicHost = devMode ? "http://localhost:8080" : "";

module.exports = function (env, args) {
    return {
        context: __dirname,
        entry: {
            "main": ["./assets/js/main.js"]
        },
        output: {
            path: buildPath,
            publicPath: publicHost + "/static/build/",
            filename: devMode ? "[name].js" : "[name].[hash].js",
            chunkFilename: devMode ? "[id].js" : "[id].[chunkhash].js",
        },
        module: {
            rules: [
                {
                    test: /\.js$/,
                    use: "babel-loader",
                    exclude: /node_modules/
                },
                {
                    test: /\.vue$/,
                    use: "vue-loader",
                    exclude: /node_modules/
                },
                {
                    test: /\.css$/,
                    use: [devMode ? "style-loader" : MiniCssExtractPlugin.loader, "css-loader"]
                },
                {
                    test: /\.(png)|(jpg)|(gif)|(woff)|(svg)|(eot)|(ttf)$/,
                    use: "url-loader"
                },
                {
                    test: /\.styl$/,
                    use: [devMode ? "style-loader" : MiniCssExtractPlugin.loader, "css-loader", "stylus-loader"]
                }
            ]
        },
        optimization: {
            splitChunks: {
                chunks: "all",
                minChunks: 1,
                cacheGroups: {
                    vendor: {
                        test: /[\\/]node_modules[\\/]/,
                        name: "vendor",
                    }
                }
            }
        },
        plugins: [
            new webpack.ProvidePlugin({
            }),

            new CleanWebpackPlugin([buildPath]),

            new MiniCssExtractPlugin({
                filename: devMode ? "[name].css" : "[name].[hash].css",
                chunkFilename: devMode ? "[id].css" : "[id].[chunkhash].css"
            }),

            new ManifestRevisionPlugin(path.join("./app/webpack", "manifest.json"), {
                rootAssetPath: rootAssetPath
            })
        ],
        resolve: {
            extensions: [".js"]
        },
        mode: devMode ? "development" : "production"
    }
};
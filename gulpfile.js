'use strict';
var gulp = require('gulp');
var sass = require('gulp-sass');
var minifycss = require('gulp-minify-css');
var autoprefixer = require('gulp-autoprefixer');
var sourcemaps = require('gulp-sourcemaps');

var paths = {
    sass: 'wye/static/sass/*.sass',
    css: 'wye/static/css/*.css'
};

gulp.task('css', function() {
    return gulp.src(paths.sass)
        .pipe(sourcemaps.init())
            .pipe(sass({
                indentedSyntax: true
            }).on('error', sass.logError))
            .pipe(autoprefixer({
                browsers: ['> 1%']
            }))
            .pipe(minifycss({
                debug: true
            }))
        .pipe(sourcemaps.write('.'))
        .pipe(gulp.dest(paths.css));
});

gulp.task('watch', function() {
    gulp.watch(paths.sass, ['css']);
});

gulp.task('default', ['watch']);

import path from 'path';
import sourcemaps from 'rollup-plugin-sourcemaps';
import summary from 'rollup-plugin-summary';
import {terser} from 'rollup-plugin-terser';
import commonjs from '@rollup/plugin-commonjs';
import resolve from '@rollup/plugin-node-resolve';
import babel from '@rollup/plugin-babel';
import styles from "rollup-plugin-styles";
import svg from 'rollup-plugin-svg';


export default {
  input: 'client/django-formset.ts',
  output: {
    dir: 'formset/static/formset/js/',
    format: 'esm',
    sourcemap: true,
  },
  onwarn(warning) {
    if (warning.code !== 'THIS_IS_UNDEFINED') {
      console.error(`(!) ${warning.message}`);
    }
  },
  plugins: [
    resolve({
      extensions: ['.ts', '.svg', '.scss', '.js']
    }),
    styles(),
    svg(),
    commonjs(),
    babel({
      babelHelpers: 'bundled',
      configFile: path.resolve(__dirname, 'babel.config.json'),
      extensions: ['.ts'],
    }),
    sourcemaps(),
    terser({
      ecma: 2017,
      module: true,
      warnings: true,
      mangle: {
        properties: {
          regex: /^__/,
        },
      },
    }),
    summary(),
  ],
};

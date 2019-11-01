<template lang="pug">
div(@click.self='close')

  span.toggle.pointer(@click='toggle')
    span(v-if='obj(value)') {{ isOpen ? '\u2b9f': '\u2b9e' }}
  span.key(
    @click='toggle' :class='{pointer: obj(value)}' :data-type='typeof name' :data-content='name'
    ) {{ name + ': ' }}

  template(v-if='notObj(value)')
    span.value(:data-type='typeof value' :data-content='value' :data-key='name') {{ value }}
  span.preview(v-else-if='!isOpen' @click='toggle')
    | {{ '\u00A0'.repeat(3) + preview.string + (preview.full ? '' : ' ...' )}}
  div.indent(v-else)
    template(v-for='[key, val] of children')
      JSONRenderer(:name='key' :value='val' :key='key')


</template>
<script>
export default {
  name: "JSONRenderer",
  props: {
    name: { required: false },
    value: { required: true }
  },
  methods: {
    notObj(val) {
      return typeof val !== "object";
    },
    obj(val) {
      return !this.notObj(val);
    },
    toggle() {
      this.$store.commit("setOpen", { name: this.name, val: !this.isOpen });
    },
    close() {
      if (this.isOpen)
        this.$store.commit("setOpen", { name: this.name, val: false });
    }
  },
  computed: {
    isOpen() {
      return this.$store.getters.isOpen(this.name);
    },
    preview() {
      const str = JSON.stringify(this.value);
      return { string: str.slice(0, 50), full: str.length < 50 };
    },
    children() {
      if (Array.isArray(this.value)) return this.value.map((e, i) => [i, e]);

      return Object.entries(this.value);
    }
  }
};
</script>

<style lang="scss" scoped>
$lime: rgb(155, 236, 174);
$red: rgb(200, 0, 0);
$purple: rgb(153, 128, 255);

.toggle {
  display: inline-block;
  width: 20px;
}
.pointer {
  cursor: pointer;
}
.indent {
  padding-left: 30px;
}

.preview {
  color: #666666;
}

.key[data-type="number"] {
  color: $purple;
}
.value[data-type="number"] {
  &[data-key="population"] {
    color: $lime;
  }
  color: $purple;
}

.value[data-type="string"] {
  &[data-content="win"] {
    color: $lime;
  }

  &[data-content="lose"] {
    color: $red;
  }

  @function reverse($list) {
    $result: ();
    @for $i from length($list) * -1 through -1 {
      $result: append($result, nth($list, abs($i)));
    }
    @return $result;
  }

  $colors: red, red, yellow, chartreuse, chartreuse;
  $ratings: "--", "-", "o", "+", "++";
  $cityKeys: "economy", "government", "hygiene", "awareness";
  $pathogenKeys: "infectivity", "mobility", "duration", "lethality";
  $size: large;

  @each $key in $cityKeys {
    @each $rating in $ratings {
      $index: index($ratings, $rating);
      $color: nth($colors, $index);

      &[data-key="#{$key}"] {
        &[data-content="#{$rating}"] {
          font-size: $size;
          color: $color;
        }
      }
    }
  }

  @each $key in $pathogenKeys {
    $reversedColors: reverse($colors);
    @each $rating in $ratings {
      $index: index($ratings, $rating);
      $color: nth($reversedColors, $index);

      &[data-key="#{$key}"] {
        &[data-content="#{$rating}"] {
          font-size: $size;
          color: $color;
        }
      }
    }
  }
}

</style>

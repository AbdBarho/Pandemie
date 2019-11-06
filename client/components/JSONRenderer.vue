<template lang="pug">
div(@click.self='close')
  template(v-if='onlyChildren')
    JSONRenderer(v-for='[key, val] of children' :name='key' :value='val' :parentKey='openKey' :key='key')
  template(v-else)
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
        JSONRenderer(v-for='[key, val] of children' :name='key' :value='val' :parentKey='openKey' :key='key')


</template>
<script>
export default {
  name: "JSONRenderer",
  props: {
    name: { required: false },
    value: { required: true },
    parentKey: { required: false, default: "" },
    onlyChildren: { required: false, default: false }
  },
  methods: {
    notObj(val) {
      return typeof val !== "object";
    },
    obj(val) {
      return !this.notObj(val);
    },
    setOpen(val) {
      this.$store.commit("setOpen", { name: this.openKey, val });
    },
    toggle() {
      this.setOpen(!this.isOpen);
    },
    close() {
      if (this.isOpen) this.setOpen(false);
    }
  },
  computed: {
    openKey() {
      return `${this.parentKey}/${this.name}`;
    },
    isOpen() {
      return this.$store.getters.isOpen(this.openKey);
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
@import "./styles/colors.scss";

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
  color: $greyOut;
}
</style>

<template>
  <transition name="slide">
    <div v-if="isOpen" class="filter-overlay" @click.self="close">
      <div class="filter-backdrop" @click="close"></div>
      <div class="filter-bar">
        <div class="filter-header">
          <span>FILTERS</span><span class="close" @click="close">✕</span>
        </div>

        <div class="filter-section">
          <label class="label">SORT BY</label>
          <select v-model="draftSort">
            <option value="newest">Newest</option>
            <option value="collected">Collected</option>
            <option value="relevance">Relevance</option>
            <option value="words">Words</option>
          </select>
        </div>

        <div class="filter-section">
          <label class="label">CATEGORY</label>
          <div class="category-list">
            <label v-for="cat in categories" :key="cat" class="check">
              <input
                type="checkbox"
                :checked="draftCategories.includes(cat)"
                @change="toggleCategory(cat)"
              />
              {{ cat }}
            </label>
          </div>
        </div>

        <div class="filter-section">
          <label class="label">AUTHOR</label>
          <select v-model="draftAuthor">
            <option value="">All Authors</option>
            <option v-for="a in authors" :key="a" :value="a">{{ a }}</option>
          </select>
        </div>

        <div class="filter-section">
          <label class="label">PUBLISHED DATE</label>
          <div class="date-range">
            <input type="date" v-model="draftDateFrom" :max="draftDateTo || undefined" />
            <span class="date-sep">to</span>
            <input type="date" v-model="draftDateTo" :min="draftDateFrom || undefined" />
          </div>
        </div>

        <div class="filter-section">
          <div class="filter-actions">
            <button class="btn-clear-full" @click="handleClear">CLEAR ALL FILTERS</button>
            <button class="btn-apply" @click="handleApply">FILTER</button>
          </div>
        </div>
      </div>
    </div>
  </transition>
</template>

<script setup>
import { ref, watch } from "vue";

const props = defineProps({
  isOpen: { type: Boolean, required: true },
  sort: { type: String, required: true },
  categories: { type: Array, required: true },      // all available category values
  authors: { type: Array, required: true },          // all available author values
  selectedCategories: { type: Array, required: true },
  selectedAuthor: { type: String, required: true },
  dateFrom: { type: String, required: true },        // 'YYYY-MM-DD' or ''
  dateTo: { type: String, required: true },          // 'YYYY-MM-DD' or ''
});

const emit = defineEmits(["apply", "clear", "close"]);

// Local "draft" copies — editing these does NOT affect the actual filtered list
const draftSort = ref(props.sort);
const draftCategories = ref([...props.selectedCategories]);
const draftAuthor = ref(props.selectedAuthor);
const draftDateFrom = ref(props.dateFrom);
const draftDateTo = ref(props.dateTo);

// Re-sync drafts from the live/applied values whenever the panel is reopened
watch(
  () => props.isOpen,
  (open) => {
    if (open) {
      draftSort.value = props.sort;
      draftCategories.value = [...props.selectedCategories];
      draftAuthor.value = props.selectedAuthor;
      draftDateFrom.value = props.dateFrom;
      draftDateTo.value = props.dateTo;
    }
  }
);

function toggleCategory(cat) {
  draftCategories.value = draftCategories.value.includes(cat)
    ? draftCategories.value.filter((c) => c !== cat)
    : [...draftCategories.value, cat];
}

function handleApply() {
  emit("apply", {
    sort: draftSort.value,
    categories: draftCategories.value,
    author: draftAuthor.value,
    dateFrom: draftDateFrom.value,
    dateTo: draftDateTo.value,
  });
  emit("close");
}

function handleClear() {
  draftSort.value = "newest";
  draftCategories.value = [];
  draftAuthor.value = "";
  draftDateFrom.value = "";
  draftDateTo.value = "";
  emit("clear");
  emit("close");
}

function close() {
  emit("close");
}
</script>

<style scoped>
.filter-overlay { position: fixed; inset: 0; z-index: 100; }
.filter-backdrop { position: fixed; inset: 0; background: rgba(17, 17, 17, 0.15); backdrop-filter: blur(16px) saturate(1.1); -webkit-backdrop-filter: blur(16px) saturate(1.1); }
.filter-bar { position: absolute; left: 16px; top: 12px; width: 300px; max-height: calc(100vh - 140px); background: #fffbf7; border: 1.5px solid #111; box-shadow: 0 20px 50px rgba(0, 0, 0, 0.25); z-index: 101; overflow-y: auto; font-family: "IBM Plex Mono", monospace; }
.filter-header { display: flex; justify-content: space-between; padding: 14px 16px; font-size: 10px; font-weight: 700; letter-spacing: 0.08em; border-bottom: 1px solid #e5e2de; background: #fff; }
.close { cursor: pointer; border: 1px solid #e5e2de; width: 22px; height: 22px; display: flex; align-items: center; justify-content: center; background: #fff; }
.filter-section { padding: 16px; border-bottom: 1px solid #f0ede8; }
.label { font-size: 9px; color: #999; letter-spacing: 0.08em; margin-bottom: 10px; display: block; text-transform: uppercase; }
select { width: 100%; height: 36px; border: 1px solid #e5e2de; background: #fff; padding: 0 10px; font-family: inherit; font-size: 11px; outline: none; cursor: pointer; }
.category-list { display: flex; flex-direction: column; gap: 2px; margin-top: 8px; }
.check { display: flex; gap: 8px; align-items: center; font-size: 11px; padding: 6px 0; cursor: pointer; color: #333; }
.date-range { display: flex; align-items: center; gap: 6px; margin-top: 8px; }
.date-range input[type="date"] { flex: 1; border: 1px solid #e5e2de; background: #fff; padding: 6px 8px; font-family: inherit; font-size: 11px; outline: none; }
.date-sep { font-size: 10px; color: #999; }
.filter-actions { display: flex; gap: 8px; padding: 16px; }
.btn-clear-full, .btn-apply { flex: 1; height: 38px; border: 1.5px solid #111; font-family: inherit; font-size: 10px; font-weight: 700; letter-spacing: 0.06em; cursor: pointer; }
.btn-clear-full { background: #fff; }
.btn-apply { background: #111; color: #fff; }
.slide-enter-active, .slide-leave-active { transition: transform 0.25s ease, opacity 0.25s ease; }
.slide-enter-from, .slide-leave-to { transform: translateY(-10px) translateX(-10px); opacity: 0; }
</style>
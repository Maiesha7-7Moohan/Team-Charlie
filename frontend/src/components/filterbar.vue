<template>
 <Transition name="slide">
    <div
      v-if="isOpen"
      class="filter-overlay"
      @click.self="emit('close')"
    >
 <div class="filter-bar">
 <div class="filter-header">
 <span>FILTERS</span
              ><span class="close" @click="emit('close')">✕</span>
              </div>
       <div class="filter-section">
      <div class="search-input">
       <span>⌕</span
       ><input
 :value="search"
 @input="
  emit('update:search', ($event.target as HTMLInputElement).value)
 "
placeholder="Search..."
/>
</div>
</div>
<div class="filter-section">
<label class="label">SORT BY</label
><select
:value="sort"
@change="
emit('update:sort', ($event.target as HTMLSelectElement).value)
"
>
<option value="newest">Newest</option>
<option value="collected">Collected</option>
<option value="relevance">Relevance</option>
</select>
</div>
<div class="filter-section">
<label class="label">CATEGORY</label>
<div class="category-list">
<template v-for="categoryItem in categories" :key="categoryItem">
<div
class="cat-item"
:class="{ active: category === categoryItem }"
@click="emit('update:category', categoryItem)"
>
{{ categoryItem }}
</div>
</template>
</div>
</div>
<div class="filter-section">
<label class="label">STATUS</label
><label v-for="s in statusOptions" :key="s" class="check"
><input
type="checkbox"
:checked="status.includes(s)"
@change="toggleStatus(s)"
/>
{{ s }}</label
>
</div>
<div class="filter-section">
<label class="label">PRIORITY</label
><label v-for="p in priorityOptions" :key="p" class="check"
><input
type="checkbox"
:checked="priority.includes(p)"
@change="togglePriority(p)"
/>
{{ p }}</label
>
</div>
<div class="filter-actions">
<button
class="btn-clear-full"
@click="handleClear"
>
CLEAR ALL FILTERS
</button>
</div>
</div>
</div>
</Transition>
</template>

<script setup lang="ts">
const props = defineProps<{
isOpen: boolean;
search: string;
sort: string;
category: string;
status: string[];
priority: string[];
}>();
const emit = defineEmits([
"update:search",
"update:sort",
"update:category",
"update:status",
"update:priority",
"clear",
"close",
]);
const categories = [
"All Sources",
"Reuters",
"AP News",
"BBC",
"The Guardian",
"Bloomberg",
"Politico",
"Al Jazeera",
];
const statusOptions = ["Active", "In Review", "Blocked", "Closed"];
const priorityOptions = ["Critical", "High", "Medium", "Low"];
function toggleStatus(val: string) {
const n = props.status.includes(val)
? props.status.filter((v) => v !== val)
: [...props.status, val];
emit("update:status", n);
}
function togglePriority(val: string) {
const n = props.priority.includes(val)
? props.priority.filter((v) => v !== val)
: [...props.priority, val];
emit("update:priority", n);
}

function handleClear() {
  emit("clear");
  emit("close");
}
</script>

<style scoped>
.filter-overlay {
  position: fixed;
  inset: 0;
  z-index: 100;
}

.filter-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(17, 17, 17, 0.15);
  backdrop-filter: blur(16px) saturate(1.1);
  -webkit-backdrop-filter: blur(16px) saturate(1.1);
}

.filter-bar {
  position: absolute;
  left: 16px;
  top: 12px;
  width: 300px;
  max-height: calc(100vh - 140px);
  background: #FFFBF7;
  border: 1.5px solid #111;
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.25);
  z-index: 101;
  overflow-y: auto;
  font-family: "IBM Plex Mono", monospace;
}
.filter-header {
  display: flex;
  justify-content: space-between;
  padding: 14px 16px;
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.08em;
  border-bottom: 1px solid #E5E2DE;
  background: #fff;
}
.close {
  cursor: pointer;
  border: 1px solid #E5E2DE;
  width: 22px;
  height: 22px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #fff;
}
.filter-section {
  padding: 16px;
  border-bottom: 1px solid #F0EDE8;
}
.label {
  font-size: 9px;
  color: #999;
  letter-spacing: 0.08em;
  margin-bottom: 10px;
  display: block;
  text-transform: uppercase;
}
.search-input {
  display: flex;
  align-items: center;
  gap: 8px;
  border: 1px solid #E5E2DE;
  background: #fff;
  padding: 8px 10px;
}
.search-input input {
  border: none;
  outline: none;
  font-size: 12px;
  font-family: inherit;
  width: 100%;
  background: transparent;
}
select {
  width: 100%;
  height: 36px;
  border: 1px solid #E5E2DE;
  background: #fff;
  padding: 0 10px;
  font-family: inherit;
  font-size: 11px;
  outline: none;
  cursor: pointer;
}
.category-list {
  display: flex;
  flex-direction: column;
  gap: 2px;
  margin-top: 8px;
}
.cat-item {
  padding: 7px 8px;
  font-size: 11px;
  cursor: pointer;
  color: #666;
  border-radius: 2px;
}
.cat-item:hover {
  background: #fff;
}
.cat-item.active {
  background: #111;
  color: #fff;
  font-weight: 600;
}
.check {
  display: flex;
  gap: 8px;
  align-items: center;
  font-size: 11px;
  padding: 6px 0;
  cursor: pointer;
  color: #333;
}
.filter-actions {
  padding: 16px;
}
.btn-clear-full {
  width: 100%;
  height: 38px;
  border: 1.5px solid #111;
  background: #fff;
  font-family: inherit;
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.06em;
  cursor: pointer;
}
.slide-enter-active,
.slide-leave-active {
  transition:
    transform 0.25s ease,
    opacity 0.25s ease;
}
.slide-enter-from,
.slide-leave-to {
  transform: translateY(-10px) translateX(-10px);
  opacity: 0;
}
</style>
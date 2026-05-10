export default function App() {
  return (
    <div className="size-full flex items-center justify-center bg-white">
      <div className="w-[800px] h-[600px] flex items-center justify-center">
        <div
          className="w-[420px] rounded-lg border border-[#B0B0B0] bg-white overflow-hidden"
          style={{ boxShadow: '0 2px 8px rgba(0, 0, 0, 0.08)' }}
        >
          {/* Table Header */}
          <div className="h-12 bg-[#F3F4F6] border-b border-[#B0B0B0] flex items-center justify-center">
            <h2 className="text-base font-semibold text-[#111827]">ufo_sightings</h2>
          </div>

          {/* Column List */}
          <div className="px-4 py-4 space-y-1">
            <div className="text-sm leading-5 text-[#111827] font-semibold">id (PK)</div>
            <div className="text-sm leading-5 text-[#111827]">date_time</div>
            <div className="text-sm leading-5 text-[#111827]">city</div>
            <div className="text-sm leading-5 text-[#111827]">state</div>
            <div className="text-sm leading-5 text-[#111827]">country</div>
            <div className="text-sm leading-5 text-[#111827]">shape</div>
            <div className="text-sm leading-5 text-[#111827]">encounter_length</div>
            <div className="text-sm leading-5 text-[#111827]">duration_text</div>
            <div className="text-sm leading-5 text-[#111827]">summary</div>
            <div className="text-sm leading-5 text-[#111827]">latitude</div>
            <div className="text-sm leading-5 text-[#111827]">longitude</div>
          </div>

          {/* Optional Annotation */}
          <div className="px-4 pb-4 pt-2 border-t border-[#E5E7EB]">
            <div className="text-xs text-[#6B7280] space-y-0.5">
              <div>Primary key: <span className="font-medium">id</span></div>
              <div>Indexed columns: <span className="font-medium">date_time, state, country, shape</span></div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

import { useState } from "react";
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend,
  PieChart, Pie, Cell, LineChart, Line, ResponsiveContainer, RadarChart,
  Radar, PolarGrid, PolarAngleAxis, PolarRadiusAxis
} from "recharts";

const COLORS = {
  explicit: "#e63946",
  clean: "#2ec4b6",
  album: "#f4a261",
  single: "#457b9d",
  accent: "#ffd166",
  bg: "#0d0f14",
  card: "#161b22",
  border: "#21262d",
  text: "#e6edf3",
  muted: "#7d8590",
};

const explicitData = [
  { name: "Explicit", value: 56.3, count: 15640, color: COLORS.explicit },
  { name: "Clean", value: 43.7, count: 12160, color: COLORS.clean },
];
const formatData = [
  { name: "Album", value: 52.9, count: 14695, color: COLORS.album },
  { name: "Single", value: 47.1, count: 13096, color: COLORS.single },
];
const popularityComparison = [
  { category: "Explicit", popularity: 73.33, fill: COLORS.explicit },
  { category: "Clean", popularity: 80.9, fill: COLORS.clean },
  { category: "Album", popularity: 72.99, fill: COLORS.album },
  { category: "Single", popularity: 80.75, fill: COLORS.single },
];
const rankTierData = [
  { tier: "Top 10", explicit: 62.4, clean: 37.6 },
  { tier: "Top 11-25", explicit: 54.5, clean: 45.5 },
  { tier: "Top 26-50", explicit: 54.8, clean: 45.2 },
];
const durationBuckets = [
  { bucket: "Short (<2.5m)", count: 3582, popularity: 76.91 },
  { bucket: "Medium (2.5-4m)", count: 22717, popularity: 76.53 },
  { bucket: "Long (>4m)", count: 1501, popularity: 77.79 },
];
const albumSizeData = [
  { size: "Small (<=15)", popularity: 74.48 },
  { size: "Large (>15)", popularity: 70.91 },
];
const topArtists = [
  { artist: "Werenoi", appearances: 2206 },
  { artist: "PLK", appearances: 906 },
  { artist: "SDM", appearances: 901 },
  { artist: "Jul", appearances: 711 },
  { artist: "Ninho", appearances: 622 },
  { artist: "Fave", appearances: 597 },
  { artist: "Tiakola", appearances: 594 },
  { artist: "GIMS", appearances: 559 },
  { artist: "KeBlack", appearances: 546 },
  { artist: "Dua Lipa", appearances: 489 },
];
const monthlyExplicit = [
  { month: "May'24", explicit: 56.9 },
  { month: "Jun'24", explicit: 62.7 },
  { month: "Jul'24", explicit: 63.5 },
  { month: "Aug'24", explicit: 55.0 },
  { month: "Sep'24", explicit: 66.5 },
  { month: "Oct'24", explicit: 67.0 },
  { month: "Nov'24", explicit: 60.2 },
  { month: "Dec'24", explicit: 58.4 },
  { month: "Jan'25", explicit: 64.1 },
  { month: "Feb'25", explicit: 61.3 },
  { month: "Mar'25", explicit: 63.8 },
  { month: "Apr'25", explicit: 65.2 },
];
const albumTypeExplicit = [
  { type: "Album tracks", explicit: 72.4, clean: 27.6 },
  { type: "Single tracks", explicit: 38.2, clean: 61.8 },
];
const kpiData = [
  { label: "Explicit Content Share", value: "56.3%", desc: "Audience sensitivity indicator", color: COLORS.explicit },
  { label: "Clean Content Ratio", value: "43.7%", desc: "Compliance preference", color: COLORS.clean },
  { label: "Single vs Album", value: "47 / 53", desc: "Format preference", color: COLORS.single },
  { label: "Avg Song Duration", value: "3.09 min", desc: "Structural norm", color: COLORS.accent },
  { label: "Clean Track Pop Score", value: "80.9 / 100", desc: "Clean content leads", color: COLORS.clean },
  { label: "Content Acceptance Score", value: "37.6%", desc: "Clean share in Top 10", color: COLORS.album },
];
const radarData = [
  { metric: "Explicit Share", value: 56 },
  { metric: "Clean Popularity", value: 81 },
  { metric: "Single Format", value: 47 },
  { metric: "Album Explicit%", value: 72 },
  { metric: "Top10 Explicit%", value: 62 },
  { metric: "Duration Score", value: 62 },
];

const NavItem = ({ label, active, onClick }) => (
  <button onClick={onClick} style={{
    background: active ? "rgba(230,57,70,0.15)" : "transparent",
    border: active ? `1px solid ${COLORS.explicit}` : "1px solid transparent",
    color: active ? COLORS.explicit : COLORS.muted,
    padding: "8px 14px", borderRadius: "6px", cursor: "pointer",
    fontSize: "12px", fontFamily: "monospace", fontWeight: active ? 600 : 400,
    transition: "all 0.2s", whiteSpace: "nowrap",
  }}>{label}</button>
);

const Card = ({ children, style = {} }) => (
  <div style={{ background: COLORS.card, border: `1px solid ${COLORS.border}`, borderRadius: "12px", padding: "20px", ...style }}>
    {children}
  </div>
);

const SectionTitle = ({ children }) => (
  <h2 style={{ color: COLORS.text, fontFamily: "Impact, sans-serif", fontSize: "18px", letterSpacing: "2px", marginBottom: "14px", borderLeft: `3px solid ${COLORS.explicit}`, paddingLeft: "10px" }}>
    {children}
  </h2>
);

const InsightBox = ({ text, color = COLORS.explicit }) => (
  <div style={{ background: `${color}15`, border: `1px solid ${color}40`, borderLeft: `3px solid ${color}`, borderRadius: "8px", padding: "10px 14px", fontSize: "12px", color: COLORS.text, fontFamily: "monospace", lineHeight: 1.6, marginTop: "12px" }}>
    💡 {text}
  </div>
);

const CustomTooltip = ({ active, payload, label }) => {
  if (!active || !payload?.length) return null;
  return (
    <div style={{ background: "#1c2128", border: `1px solid ${COLORS.border}`, borderRadius: "8px", padding: "10px 14px", fontSize: "12px", color: COLORS.text, fontFamily: "monospace" }}>
      <p style={{ color: COLORS.muted, marginBottom: 4 }}>{label}</p>
      {payload.map((p, i) => (
        <p key={i} style={{ color: p.color || COLORS.text }}>{p.name}: <strong>{typeof p.value === "number" ? p.value.toFixed(1) : p.value}</strong></p>
      ))}
    </div>
  );
};

function OverviewPage() {
  return (
    <div>
      <div style={{ display: "grid", gridTemplateColumns: "repeat(3,1fr)", gap: "12px", marginBottom: "20px" }}>
        {kpiData.map((kpi, i) => (
          <Card key={i} style={{ textAlign: "center" }}>
            <div style={{ color: kpi.color, fontSize: "26px", fontFamily: "Impact, sans-serif", letterSpacing: "1px" }}>{kpi.value}</div>
            <div style={{ color: COLORS.text, fontSize: "11px", fontWeight: 600, marginTop: 4 }}>{kpi.label}</div>
            <div style={{ color: COLORS.muted, fontSize: "10px", marginTop: 2 }}>{kpi.desc}</div>
          </Card>
        ))}
      </div>
      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "16px" }}>
        <Card>
          <SectionTitle>CONTENT PROFILE RADAR</SectionTitle>
          <ResponsiveContainer width="100%" height={250}>
            <RadarChart data={radarData}>
              <PolarGrid stroke={COLORS.border} />
              <PolarAngleAxis dataKey="metric" tick={{ fill: COLORS.muted, fontSize: 10 }} />
              <PolarRadiusAxis angle={30} domain={[0,100]} tick={{ fill: COLORS.muted, fontSize: 9 }} />
              <Radar name="France Top 50" dataKey="value" stroke={COLORS.explicit} fill={COLORS.explicit} fillOpacity={0.3} />
            </RadarChart>
          </ResponsiveContainer>
        </Card>
        <Card>
          <SectionTitle>POPULARITY BY CONTENT TYPE</SectionTitle>
          <ResponsiveContainer width="100%" height={200}>
            <BarChart data={popularityComparison} barSize={36}>
              <CartesianGrid strokeDasharray="3 3" stroke={COLORS.border} />
              <XAxis dataKey="category" tick={{ fill: COLORS.muted, fontSize: 11 }} />
              <YAxis domain={[68,84]} tick={{ fill: COLORS.muted, fontSize: 11 }} />
              <Tooltip content={<CustomTooltip />} />
              <Bar dataKey="popularity" name="Avg Popularity" radius={[4,4,0,0]}>
                {popularityComparison.map((e,i) => <Cell key={i} fill={e.fill} />)}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
          <InsightBox text="Clean content averages 80.9 vs 73.3 for explicit — a 10.4% popularity premium. Singles (80.75) consistently beat albums (72.99)." color={COLORS.clean} />
        </Card>
      </div>
    </div>
  );
}

function ExplicitPage() {
  return (
    <div>
      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "16px", marginBottom: "16px" }}>
        <Card>
          <SectionTitle>EXPLICIT vs CLEAN SPLIT</SectionTitle>
          <ResponsiveContainer width="100%" height={220}>
            <PieChart>
              <Pie data={explicitData} cx="50%" cy="50%" innerRadius={55} outerRadius={85} dataKey="value" paddingAngle={3}>
                {explicitData.map((e,i) => <Cell key={i} fill={e.color} />)}
              </Pie>
              <Tooltip formatter={(v) => `${v}%`} contentStyle={{ background:"#1c2128", border:`1px solid ${COLORS.border}`, borderRadius:8, fontFamily:"monospace" }} />
              <Legend formatter={(v) => <span style={{ color:COLORS.text, fontSize:12 }}>{v}</span>} />
            </PieChart>
          </ResponsiveContainer>
          <div style={{ textAlign:"center", color:COLORS.muted, fontSize:"11px", fontFamily:"monospace" }}>15,640 explicit · 12,160 clean</div>
        </Card>
        <Card>
          <SectionTitle>EXPLICIT % BY RANK TIER</SectionTitle>
          <ResponsiveContainer width="100%" height={220}>
            <BarChart data={rankTierData} barSize={24}>
              <CartesianGrid strokeDasharray="3 3" stroke={COLORS.border} />
              <XAxis dataKey="tier" tick={{ fill:COLORS.muted, fontSize:11 }} />
              <YAxis domain={[0,100]} tick={{ fill:COLORS.muted, fontSize:11 }} unit="%" />
              <Tooltip content={<CustomTooltip />} />
              <Bar dataKey="explicit" name="Explicit %" fill={COLORS.explicit} radius={[4,4,0,0]} />
              <Bar dataKey="clean" name="Clean %" fill={COLORS.clean} radius={[4,4,0,0]} />
            </BarChart>
          </ResponsiveContainer>
        </Card>
      </div>
      <Card style={{ marginBottom:"16px" }}>
        <SectionTitle>EXPLICIT TREND OVER TIME</SectionTitle>
        <ResponsiveContainer width="100%" height={180}>
          <LineChart data={monthlyExplicit}>
            <CartesianGrid strokeDasharray="3 3" stroke={COLORS.border} />
            <XAxis dataKey="month" tick={{ fill:COLORS.muted, fontSize:10 }} />
            <YAxis domain={[50,72]} unit="%" tick={{ fill:COLORS.muted, fontSize:11 }} />
            <Tooltip content={<CustomTooltip />} />
            <Line type="monotone" dataKey="explicit" name="Explicit %" stroke={COLORS.explicit} strokeWidth={2.5} dot={{ fill:COLORS.explicit, r:4 }} />
          </LineChart>
        </ResponsiveContainer>
        <InsightBox text="Top 10 holds the highest explicit share (62.4%). French listeners don't penalize explicit content in rankings — but clean tracks still command higher popularity scores overall." />
      </Card>
      <Card>
        <SectionTitle>EXPLICIT SPLIT BY FORMAT</SectionTitle>
        <ResponsiveContainer width="100%" height={160}>
          <BarChart data={albumTypeExplicit} layout="vertical" barSize={22}>
            <CartesianGrid strokeDasharray="3 3" stroke={COLORS.border} />
            <XAxis type="number" domain={[0,100]} unit="%" tick={{ fill:COLORS.muted, fontSize:11 }} />
            <YAxis dataKey="type" type="category" width={100} tick={{ fill:COLORS.muted, fontSize:11 }} />
            <Tooltip content={<CustomTooltip />} />
            <Bar dataKey="explicit" name="Explicit %" fill={COLORS.explicit} stackId="a" radius={[0,4,4,0]} />
            <Bar dataKey="clean" name="Clean %" fill={COLORS.clean} stackId="a" radius={[0,4,4,0]} />
          </BarChart>
        </ResponsiveContainer>
        <InsightBox text="72.4% of album tracks are explicit vs only 38.2% of singles. Atlantic RC should apply stricter compliance checks to album releases targeting France." color={COLORS.album} />
      </Card>
    </div>
  );
}

function FormatPage() {
  return (
    <div>
      <div style={{ display:"grid", gridTemplateColumns:"1fr 1fr", gap:"16px", marginBottom:"16px" }}>
        <Card>
          <SectionTitle>SINGLE vs ALBUM SPLIT</SectionTitle>
          <ResponsiveContainer width="100%" height={220}>
            <PieChart>
              <Pie data={formatData} cx="50%" cy="50%" outerRadius={80} dataKey="value" paddingAngle={4} label={({name,value}) => `${name} ${value}%`}>
                {formatData.map((e,i) => <Cell key={i} fill={e.color} />)}
              </Pie>
              <Tooltip formatter={(v) => `${v}%`} contentStyle={{ background:"#1c2128", border:`1px solid ${COLORS.border}`, fontFamily:"monospace", borderRadius:8 }} />
            </PieChart>
          </ResponsiveContainer>
        </Card>
        <Card>
          <SectionTitle>FORMAT POPULARITY</SectionTitle>
          <div style={{ padding:"16px 0", display:"flex", flexDirection:"column", gap:"16px" }}>
            {[{ label:"Single avg popularity", value:80.75, color:COLORS.single }, { label:"Album avg popularity", value:72.99, color:COLORS.album }].map((item,i) => (
              <div key={i}>
                <div style={{ display:"flex", justifyContent:"space-between", marginBottom:6 }}>
                  <span style={{ color:COLORS.text, fontSize:"12px", fontFamily:"monospace" }}>{item.label}</span>
                  <span style={{ color:item.color, fontWeight:700 }}>{item.value}</span>
                </div>
                <div style={{ background:COLORS.border, borderRadius:4, height:8 }}>
                  <div style={{ background:item.color, width:`${item.value}%`, height:"100%", borderRadius:4 }} />
                </div>
              </div>
            ))}
            <InsightBox text="Singles outperform albums by +10.6 popularity points. French listeners favor concentrated releases." color={COLORS.single} />
          </div>
        </Card>
      </div>
      <Card style={{ marginBottom:"16px" }}>
        <SectionTitle>ALBUM SIZE IMPACT</SectionTitle>
        <ResponsiveContainer width="100%" height={170}>
          <BarChart data={albumSizeData} barSize={50}>
            <CartesianGrid strokeDasharray="3 3" stroke={COLORS.border} />
            <XAxis dataKey="size" tick={{ fill:COLORS.muted, fontSize:11 }} />
            <YAxis domain={[68,78]} tick={{ fill:COLORS.muted, fontSize:11 }} />
            <Tooltip content={<CustomTooltip />} />
            <Bar dataKey="popularity" name="Avg Popularity" fill={COLORS.album} radius={[4,4,0,0]} />
          </BarChart>
        </ResponsiveContainer>
        <InsightBox text="Album dilution confirmed: large albums (>15 tracks) avg 70.91 vs 74.48 for smaller projects (-4.8%). French listeners reward curated, focused albums." color={COLORS.album} />
      </Card>
      <Card>
        <SectionTitle>TRACK COUNT DISTRIBUTION</SectionTitle>
        <div style={{ display:"flex", flexWrap:"wrap", gap:"10px" }}>
          {[{tracks:"1 (Single)",count:11335,pct:40.8},{tracks:"15 tracks",count:2698,pct:9.7},{tracks:"10 tracks",count:1471,pct:5.3},{tracks:"17 tracks",count:1454,pct:5.2},{tracks:"14 tracks",count:1344,pct:4.8},{tracks:"16 tracks",count:1267,pct:4.6}].map((item,i) => (
            <div key={i} style={{ background:i===0?`${COLORS.single}20`:`${COLORS.album}15`, border:`1px solid ${i===0?COLORS.single:COLORS.album}40`, borderRadius:8, padding:"10px 14px", textAlign:"center", minWidth:100 }}>
              <div style={{ color:i===0?COLORS.single:COLORS.album, fontSize:"20px", fontFamily:"Impact" }}>{item.pct}%</div>
              <div style={{ color:COLORS.text, fontSize:"11px", fontFamily:"monospace" }}>{item.tracks}</div>
              <div style={{ color:COLORS.muted, fontSize:"10px" }}>{item.count.toLocaleString()}</div>
            </div>
          ))}
        </div>
      </Card>
    </div>
  );
}

function DurationPage() {
  return (
    <div>
      <div style={{ display:"grid", gridTemplateColumns:"repeat(3,1fr)", gap:"12px", marginBottom:"16px" }}>
        {durationBuckets.map((b,i) => (
          <Card key={i} style={{ textAlign:"center" }}>
            <div style={{ color:[COLORS.single,COLORS.clean,COLORS.album][i], fontSize:"26px", fontFamily:"Impact" }}>{b.count.toLocaleString()}</div>
            <div style={{ color:COLORS.text, fontSize:"11px", marginTop:4, fontFamily:"monospace" }}>{b.bucket}</div>
            <div style={{ color:COLORS.muted, fontSize:"11px", marginTop:4 }}>Avg popularity: {b.popularity}</div>
          </Card>
        ))}
      </div>
      <Card style={{ marginBottom:"16px" }}>
        <SectionTitle>DURATION DISTRIBUTION</SectionTitle>
        <ResponsiveContainer width="100%" height={190}>
          <BarChart data={durationBuckets} barSize={45}>
            <CartesianGrid strokeDasharray="3 3" stroke={COLORS.border} />
            <XAxis dataKey="bucket" tick={{ fill:COLORS.muted, fontSize:11 }} />
            <YAxis tick={{ fill:COLORS.muted, fontSize:11 }} />
            <Tooltip content={<CustomTooltip />} />
            <Bar dataKey="count" name="Track Entries" radius={[4,4,0,0]}>
              <Cell fill={COLORS.single} /><Cell fill={COLORS.clean} /><Cell fill={COLORS.album} />
            </Bar>
          </BarChart>
        </ResponsiveContainer>
        <InsightBox text="81.7% of all chart entries are medium-length (2.5-4 min). French listeners strongly prefer the classic pop song format. Avg duration = 3.09 min." />
      </Card>
      <Card>
        <SectionTitle>DURATION vs POPULARITY</SectionTitle>
        <ResponsiveContainer width="100%" height={190}>
          <BarChart data={durationBuckets} barSize={45}>
            <CartesianGrid strokeDasharray="3 3" stroke={COLORS.border} />
            <XAxis dataKey="bucket" tick={{ fill:COLORS.muted, fontSize:11 }} />
            <YAxis domain={[74,80]} tick={{ fill:COLORS.muted, fontSize:11 }} />
            <Tooltip content={<CustomTooltip />} />
            <Bar dataKey="popularity" name="Avg Popularity" radius={[4,4,0,0]}>
              <Cell fill={COLORS.single} /><Cell fill={COLORS.clean} /><Cell fill={COLORS.album} />
            </Bar>
          </BarChart>
        </ResponsiveContainer>
        <InsightBox text="Duration has minimal impact on popularity (range: 76.53-77.79). Content type and format matter far more than song length." color={COLORS.clean} />
      </Card>
    </div>
  );
}

function ArtistsPage() {
  return (
    <div>
      <Card style={{ marginBottom:"16px" }}>
        <SectionTitle>TOP 10 ARTISTS BY CHART APPEARANCES</SectionTitle>
        <ResponsiveContainer width="100%" height={260}>
          <BarChart data={topArtists} layout="vertical" barSize={18}>
            <CartesianGrid strokeDasharray="3 3" stroke={COLORS.border} />
            <XAxis type="number" tick={{ fill:COLORS.muted, fontSize:11 }} />
            <YAxis dataKey="artist" type="category" width={80} tick={{ fill:COLORS.text, fontSize:11, fontFamily:"monospace" }} />
            <Tooltip content={<CustomTooltip />} />
            <Bar dataKey="appearances" name="Chart Days" radius={[0,4,4,0]}>
              {topArtists.map((_,i) => <Cell key={i} fill={i===0?COLORS.explicit:i<3?COLORS.album:COLORS.single} />)}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
        <InsightBox text="Werenoi dominates with 2,206 chart appearances — 2.4x the next artist (PLK). Deep catalog longevity defines France's chart ecosystem." />
      </Card>
      <div style={{ display:"grid", gridTemplateColumns:"1fr 1fr", gap:"16px" }}>
        <Card>
          <SectionTitle>CATALOGUE STATS</SectionTitle>
          <div>
            {[{label:"Top 3 artists share",value:"14.4%",sub:"of all chart days",color:COLORS.explicit},{label:"Top 10 artists share",value:"30.4%",sub:"of all chart days",color:COLORS.album},{label:"Total unique artists",value:"500+",sub:"over 555 days",color:COLORS.clean},{label:"Dataset total entries",value:"27,800",sub:"rows analyzed",color:COLORS.accent}].map((item,i) => (
              <div key={i} style={{ display:"flex", justifyContent:"space-between", alignItems:"center", padding:"10px 0", borderBottom:`1px solid ${COLORS.border}` }}>
                <div>
                  <div style={{ color:COLORS.text, fontSize:"12px", fontFamily:"monospace" }}>{item.label}</div>
                  <div style={{ color:COLORS.muted, fontSize:"10px" }}>{item.sub}</div>
                </div>
                <div style={{ color:item.color, fontSize:"20px", fontFamily:"Impact" }}>{item.value}</div>
              </div>
            ))}
          </div>
        </Card>
        <Card>
          <SectionTitle>MARKET INSIGHTS</SectionTitle>
          <div style={{ display:"flex", flexDirection:"column", gap:"10px", paddingTop:"4px" }}>
            {[{icon:"🇫🇷",text:"French rap dominates — Werenoi, PLK, SDM, Ninho lead catalog longevity",color:COLORS.explicit},{icon:"🌍",text:"International acts appear via high-popularity single spikes, not sustained albums",color:COLORS.clean},{icon:"📀",text:"Album-releasing artists maintain chart presence 2-3x longer than single artists",color:COLORS.album},{icon:"🎯",text:"Atlantic RC should target French rap collabs for sustained playlist presence",color:COLORS.accent}].map((item,i) => (
              <div key={i} style={{ background:`${item.color}10`, border:`1px solid ${item.color}30`, borderRadius:8, padding:"10px 12px", fontSize:"12px", color:COLORS.text, fontFamily:"monospace", lineHeight:1.5 }}>
                {item.icon} {item.text}
              </div>
            ))}
          </div>
        </Card>
      </div>
    </div>
  );
}

function RecommendationsPage() {
  const recs = [
    { id:"R1", title:"Prioritize Clean Singles for French Market", detail:"Clean singles score 80.75 vs 73.33 for explicit content. For maximum chart performance and playlist pitching, lead with clean edits of all France-targeted releases.", impact:"HIGH", color:COLORS.clean },
    { id:"R2", title:"Keep Albums Focused (<=15 Tracks)", detail:"Albums >15 tracks avg 70.91 popularity vs 74.48 for leaner projects. Avoid album bloat — the French audience rewards curated collections over sprawling releases.", impact:"HIGH", color:COLORS.album },
    { id:"R3", title:"Target 2.5-4 Minute Song Duration", detail:"81.7% of all France Top 50 entries fall in the 2.5-4 min window. Ensure Atlantic RC artists avoid both overly short and excessively long cuts when targeting France.", impact:"MEDIUM", color:COLORS.accent },
    { id:"R4", title:"Audit Explicit Content in Album Rollouts", detail:"72.4% of album tracks are explicit. While explicit content does reach Top 10 (62.4%), clean albums perform measurably better. Provide clean versions for all French pitches.", impact:"HIGH", color:COLORS.explicit },
    { id:"R5", title:"Leverage French Rap Collaborations", detail:"Werenoi, PLK, SDM, Jul, and Ninho collectively dominate France's chart catalog. Atlantic RC artists should seek feature opportunities with these persistent charting artists.", impact:"MEDIUM", color:COLORS.single },
    { id:"R6", title:"Singles-First Rollout Strategy", detail:"Singles command 47% of chart share while outperforming albums by 10.6 popularity points. Release 2-3 clean singles before the album to maximize both reach and compliance.", impact:"HIGH", color:COLORS.clean },
  ];
  return (
    <div>
      <Card style={{ marginBottom:"16px", background:`${COLORS.explicit}10`, border:`1px solid ${COLORS.explicit}30` }}>
        <div style={{ display:"flex", gap:"12px", alignItems:"flex-start" }}>
          <div style={{ fontSize:"32px" }}>🎯</div>
          <div>
            <div style={{ color:COLORS.explicit, fontFamily:"Impact", fontSize:"18px", letterSpacing:"2px" }}>EXECUTIVE SUMMARY</div>
            <div style={{ color:COLORS.text, fontSize:"12px", fontFamily:"monospace", lineHeight:1.7, marginTop:6 }}>
              Based on 27,800 daily chart entries from France Top 50 Spotify playlist, Atlantic Recording Corporation should adopt a <strong>clean-singles-first, lean-album</strong> release strategy for France. While explicit content is prevalent (56.3%), clean tracks command a measurable popularity premium (+10.4%). The French market heavily favors domestic rap artists with deep catalogs over one-off hits.
            </div>
          </div>
        </div>
      </Card>
      <div style={{ display:"grid", gridTemplateColumns:"1fr 1fr", gap:"14px" }}>
        {recs.map((rec) => (
          <Card key={rec.id}>
            <div style={{ display:"flex", justifyContent:"space-between", alignItems:"center", marginBottom:8 }}>
              <div style={{ color:rec.color, fontFamily:"Impact", fontSize:"14px", letterSpacing:"2px" }}>{rec.id}</div>
              <div style={{ background:rec.impact==="HIGH"?`${COLORS.explicit}25`:`${COLORS.accent}25`, color:rec.impact==="HIGH"?COLORS.explicit:COLORS.accent, fontSize:"10px", fontFamily:"monospace", fontWeight:700, padding:"2px 8px", borderRadius:"4px" }}>{rec.impact} IMPACT</div>
            </div>
            <div style={{ color:COLORS.text, fontWeight:700, fontSize:"12px", marginBottom:6 }}>{rec.title}</div>
            <div style={{ color:COLORS.muted, fontSize:"11px", fontFamily:"monospace", lineHeight:1.6 }}>{rec.detail}</div>
          </Card>
        ))}
      </div>
    </div>
  );
}

const PAGES = [
  { key:"overview", label:"📊 Overview" },
  { key:"explicit", label:"🔞 Explicit Analysis" },
  { key:"format", label:"💿 Format Preference" },
  { key:"duration", label:"⏱ Duration" },
  { key:"artists", label:"🎤 Artists" },
  { key:"recommendations", label:"🎯 Recommendations" },
];

export default function App() {
  const [activePage, setActivePage] = useState("overview");
  const renderPage = () => {
    switch(activePage) {
      case "overview": return <OverviewPage />;
      case "explicit": return <ExplicitPage />;
      case "format": return <FormatPage />;
      case "duration": return <DurationPage />;
      case "artists": return <ArtistsPage />;
      case "recommendations": return <RecommendationsPage />;
      default: return <OverviewPage />;
    }
  };
  return (
    <div style={{ background:COLORS.bg, minHeight:"100vh", color:COLORS.text, fontFamily:"'Segoe UI', sans-serif" }}>
      <div style={{ background:COLORS.card, borderBottom:`1px solid ${COLORS.border}`, padding:"14px 20px", position:"sticky", top:0, zIndex:100 }}>
        <div style={{ display:"flex", justifyContent:"space-between", alignItems:"center", marginBottom:"12px" }}>
          <div>
            <div style={{ fontFamily:"Impact, sans-serif", fontSize:"18px", letterSpacing:"3px", background:`linear-gradient(90deg, ${COLORS.explicit}, ${COLORS.accent})`, WebkitBackgroundClip:"text", WebkitTextFillColor:"transparent" }}>
              FRANCE TOP 50 · CONTENT INTELLIGENCE
            </div>
            <div style={{ color:COLORS.muted, fontSize:"10px", fontFamily:"monospace", marginTop:2 }}>
              Atlantic Recording Corporation · 27,800 entries · 555 days · May 2024 – Nov 2025
            </div>
          </div>
          <div style={{ background:`${COLORS.explicit}15`, border:`1px solid ${COLORS.explicit}40`, borderRadius:20, padding:"3px 10px", color:COLORS.explicit, fontSize:"10px", fontFamily:"monospace", fontWeight:700 }}>LIVE ANALYSIS</div>
        </div>
        <div style={{ display:"flex", gap:"6px", flexWrap:"wrap" }}>
          {PAGES.map((p) => <NavItem key={p.key} label={p.label} active={activePage===p.key} onClick={() => setActivePage(p.key)} />)}
        </div>
      </div>
      <div style={{ padding:"20px", maxWidth:"1100px", margin:"0 auto" }}>
        {renderPage()}
      </div>
      <div style={{ textAlign:"center", padding:"14px", color:COLORS.muted, fontSize:"10px", fontFamily:"monospace", borderTop:`1px solid ${COLORS.border}` }}>
        Audience Sensitivity, Content Compliance & Format Preference Analysis · Unified Mentor Internship · Spotify France Top 50
      </div>
    </div>
  );
}

    st.write("• Clean content dominates the playlist")
    st.write("• Singles are more common than albums")
    st.write("• Medium duration songs perform better")


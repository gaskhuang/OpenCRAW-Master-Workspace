#!/usr/bin/env node
const { execSync } = require('child_process');

async function monitor() {
  console.clear();
  console.log('🦞 阿蓋小弟 - Agent 任務監控中...');
  console.log('====================================');

  try {
    // 1. 獲取所有 sessions
    const sessionsRaw = execSync('openclaw sessions list --limit 10 --json').toString();
    const sessions = JSON.parse(sessionsRaw);

    // 2. 過濾出 subagent 或是最近活躍的任務
    const activeTasks = sessions.filter(s => s.key.includes('subagent') || s.age.includes('now') || s.age.includes('sec'));

    if (activeTasks.length === 0) {
      console.log('目前沒有運作中的子任務。');
    } else {
      activeTasks.forEach(task => {
        const statusIcon = task.age.includes('now') ? '⏳' : '✅';
        console.log(`${statusIcon} [${task.key.split(':').pop()}]`);
        console.log(`   模型: ${task.model}`);
        console.log(`   狀態: ${task.age}`);
        if (task.lastMessage) {
          const lastText = task.lastMessage.substring(0, 50).replace(/\n/g, ' ');
          console.log(`   進度: ${lastText}...`);
        }
        console.log('------------------------------------');
      });
    }

    console.log('\n(每 5 秒自動更新一次，按 Ctrl+C 結束)');
  } catch (err) {
    console.log('讀取狀態中...');
  }
}

setInterval(monitor, 5000);
monitor();

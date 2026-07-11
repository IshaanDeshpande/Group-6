function quizApp() {
  return {
    answers: {
      time: null,
      transport: null,
      food: null,
      organization: null,
      teaching: null,
      group: null,
    },

    categories: [
      {
        title: 'Meal & Food Service',
        description: 'Volunteering with meals fits you well — think food pantries, community kitchens, or meal delivery routes.',
        score(a) {
          let s = 0;
          if (a.food === 'yes') s += 3;
          if (a.transport === 'yes') s += 1;
          if (a.group === 'group') s += 1;
          return s;
        },
      },
      {
        title: 'Mentorship & Tutoring',
        description: 'Teaching and mentoring roles — tutoring, workshops, or one-on-one mentoring — are a strong match for you.',
        score(a) {
          let s = 0;
          if (a.teaching === 'yes') s += 3;
          if (a.group === 'group') s += 1;
          if (a.time === '5' || a.time === '10') s += 1;
          return s;
        },
      },
      {
        title: 'Outreach & Direct Service',
        description: 'On-the-go, people-facing work — mobile outreach, deliveries, or shelter shifts — suits your setup well.',
        score(a) {
          let s = 0;
          if (a.transport === 'yes') s += 2;
          if (a.group === 'group') s += 1;
          if (a.time === '10' || a.time === '15+') s += 1;
          return s;
        },
      },
      {
        title: 'Behind-the-Scenes & Admin',
        description: 'Organizing, data entry, inventory, and scheduling — steady, independent work that keeps programs running — fits you well.',
        score(a) {
          let s = 0;
          if (a.organization === 'yes') s += 3;
          if (a.group === 'individually') s += 2;
          return s;
        },
      },
      {
        title: 'Flexible Micro-Volunteering',
        description: 'With a lighter time commitment, look for flexible, low-commitment opportunities you can do on your own schedule.',
        score(a) {
          let s = 0;
          if (a.time === '2') s += 2;
          if (a.group === 'individually') s += 1;
          if (a.transport === 'no') s += 1;
          return s;
        },
      },
      {
        title: 'Team & Community Events',
        description: 'You’re ready for a bigger, social commitment — recurring group volunteer days and community events.',
        score(a) {
          let s = 0;
          if (a.group === 'group') s += 2;
          if (a.time === '10' || a.time === '15+') s += 2;
          return s;
        },
      },
    ],

    get isComplete() {
      return Object.values(this.answers).every((v) => v !== null);
    },

    get result() {
      if (!this.isComplete) return null;
      let best = null;
      for (const category of this.categories) {
        const points = category.score(this.answers);
        if (!best || points > best.points) {
          best = { title: category.title, description: category.description, points };
        }
      }
      return best;
    },
  };
}

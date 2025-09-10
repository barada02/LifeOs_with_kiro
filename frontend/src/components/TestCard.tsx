interface TestCardProps {
  title: string;
  description: string;
  icon: string;
  color: 'blue' | 'green' | 'purple' | 'red';
}

const colorClasses = {
  blue: 'bg-blue-50 border-blue-200 text-blue-800',
  green: 'bg-green-50 border-green-200 text-green-800', 
  purple: 'bg-purple-50 border-purple-200 text-purple-800',
  red: 'bg-red-50 border-red-200 text-red-800'
};

export function TestCard({ title, description, icon, color }: TestCardProps) {
  return (
    <div className={`${colorClasses[color]} border rounded-lg p-4 hover:shadow-md transition-shadow duration-200`}>
      <div className="text-2xl mb-2">{icon}</div>
      <h3 className="font-semibold text-sm mb-1">{title}</h3>
      <p className="text-xs opacity-75">{description}</p>
    </div>
  );
}